from __future__ import annotations

import os
import json
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_INDICATOR_LIGHT,
    CONF_SIREN_PLAYER,
    CONF_SIREN_VOLUME,
    CONF_MP3_FILE,
    CONF_ENTRY_DELAY_SOUND,
    CONF_EXIT_DELAY_SOUND,
    CONF_CHIME_VOLUME,
    CONF_ENTRY_SENSORS,
    CONF_NFC_TAG,
    CONF_ALLOW_ANY_TAG,
    CONF_ACCEPT_ANY_TAG_WHEN_TRIGGERED,
    CONF_EXIT_DELAY,
    CONF_ENTRY_DELAY,
    CONF_AUTO_DISARM_TIME,
    CONF_AUTHORIZED_TAGS,
    CONF_TAG_ARMING_MODE,
    DEFAULT_ENTRY_DELAY,
    DEFAULT_EXIT_DELAY,
    DEFAULT_VOLUME,
    DEFAULT_CHIME_VOLUME,
    DEFAULT_TAG_ARMING_MODE,
    TAG_ACTION_ARM_HOME,
    TAG_ACTION_ARM_AWAY,
    SUPPORTED_AUDIO_EXTENSIONS,
)


def _scan_audio_paths(hass: HomeAssistant) -> list[str]:
    res: list[str] = []
    media_path = hass.config.path("media")
    www_path = hass.config.path("www")
    try:
        for base, prefix in [(media_path, "/media/"), (www_path, "/local/")]:
            if os.path.isdir(base):
                for root, _, files in os.walk(base):
                    for filename in files:
                        lowered = filename.lower()
                        if lowered.endswith(SUPPORTED_AUDIO_EXTENSIONS):
                            full_path = os.path.join(root, filename)
                            rel_path = (
                                prefix
                                + os.path.relpath(full_path, base).replace("\\", "/")
                            )
                            res.append(rel_path)
    except Exception:
        pass
    return sorted(res)


def _load_tags(hass: HomeAssistant) -> list[tuple[str, str]]:
    tags_file = hass.config.path(".storage", "tag")
    out: list[tuple[str, str]] = []
    try:
        with open(tags_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            items: list[dict[str, Any]] = []
            raw_data = data.get("data")
            if isinstance(raw_data, dict):
                if isinstance(raw_data.get("items"), list):
                    items = raw_data.get("items", [])
                elif isinstance(raw_data.get("tags"), list):
                    items = raw_data.get("tags", [])
            elif isinstance(raw_data, list):
                items = raw_data

            for item in items:
                tag_id = item.get("id")
                name = item.get("name") or tag_id
                if tag_id:
                    out.append((tag_id, name))
    except Exception:
        pass
    return out


def _ensure_list(value: Any) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if isinstance(value, (tuple, set)):
        return [str(item) for item in value if item]
    return [str(value)]


def _build_schema(
    data: dict[str, Any],
    audio_files: list[str],
    tags: list[tuple[str, str]],
) -> vol.Schema:
    schema_dict: dict[Any, Any] = {}

    indicator_default = data.get(CONF_INDICATOR_LIGHT)
    if indicator_default:
        indicator_default = _ensure_list(indicator_default)
    schema_dict[
        vol.Optional(CONF_INDICATOR_LIGHT, default=indicator_default)
    ] = selector.selector({"entity": {"domain": "light", "multiple": True}})
    schema_dict[vol.Optional(CONF_SIREN_PLAYER, default=data.get(CONF_SIREN_PLAYER))] = selector.selector(
        {"entity": {"domain": "media_player"}}
    )
    schema_dict[vol.Required(CONF_SIREN_VOLUME, default=data.get(CONF_SIREN_VOLUME, DEFAULT_VOLUME))] = selector.selector(
        {"number": {"min": 0, "max": 1, "step": 0.05, "mode": "slider"}}
    )

    audio_options = [
        {"label": "Kein Alarmton / No alarm sound", "value": ""}
    ] + [
        {"label": option.split("/")[-1], "value": option} for option in audio_files
    ]

    def _audio_selector():
        return selector.selector(
            {
                "select": {
                    "options": audio_options,
                    "custom_value": True,
                    "sort": False,
                }
            }
        )

    schema_dict[vol.Optional(CONF_MP3_FILE, default=data.get(CONF_MP3_FILE, ""))] = _audio_selector()
    schema_dict[vol.Optional(CONF_EXIT_DELAY_SOUND, default=data.get(CONF_EXIT_DELAY_SOUND, ""))] = _audio_selector()
    schema_dict[vol.Optional(CONF_ENTRY_DELAY_SOUND, default=data.get(CONF_ENTRY_DELAY_SOUND, ""))] = _audio_selector()
    schema_dict[vol.Required(CONF_CHIME_VOLUME, default=data.get(CONF_CHIME_VOLUME, DEFAULT_CHIME_VOLUME))] = selector.selector(
        {"number": {"min": 0, "max": 1, "step": 0.05, "mode": "slider"}}
    )

    entry_sensors_default = _ensure_list(data.get(CONF_ENTRY_SENSORS))
    schema_dict[vol.Required(CONF_ENTRY_SENSORS, default=entry_sensors_default)] = selector.selector(
        {"entity": {"domain": "binary_sensor", "multiple": True}}
    )

    tag_options = [
        {
            "label": f"{name} ({tag_id})" if name != tag_id else tag_id,
            "value": tag_id,
        }
        for tag_id, name in tags
    ]
    existing_tags = _ensure_list(data.get(CONF_AUTHORIZED_TAGS) or data.get(CONF_NFC_TAG))
    schema_dict[vol.Optional(CONF_AUTHORIZED_TAGS, default=existing_tags)] = selector.selector(
        {
            "select": {
                "options": tag_options,
                "multiple": True,
                "custom_value": False,
            }
        }
    )

    schema_dict[vol.Required(CONF_ALLOW_ANY_TAG, default=data.get(CONF_ALLOW_ANY_TAG, False))] = selector.selector(
        {"boolean": {}}
    )
    schema_dict[vol.Required(CONF_ACCEPT_ANY_TAG_WHEN_TRIGGERED, default=data.get(CONF_ACCEPT_ANY_TAG_WHEN_TRIGGERED, False))] = selector.selector(
        {"boolean": {}}
    )
    schema_dict[vol.Required(CONF_EXIT_DELAY, default=data.get(CONF_EXIT_DELAY, DEFAULT_EXIT_DELAY))] = selector.selector(
        {"number": {"min": 0, "max": 300, "mode": "box"}}
    )
    schema_dict[vol.Required(CONF_ENTRY_DELAY, default=data.get(CONF_ENTRY_DELAY, DEFAULT_ENTRY_DELAY))] = selector.selector(
        {"number": {"min": 0, "max": 300, "mode": "box"}}
    )
    auto_time = data.get(CONF_AUTO_DISARM_TIME)
    if auto_time is None or auto_time == "":
        schema_dict[vol.Optional(CONF_AUTO_DISARM_TIME)] = selector.selector({"time": {}})
    else:
        schema_dict[vol.Optional(CONF_AUTO_DISARM_TIME, default=auto_time)] = selector.selector(
            {"time": {}}
        )
    schema_dict[vol.Required(CONF_TAG_ARMING_MODE, default=data.get(CONF_TAG_ARMING_MODE, DEFAULT_TAG_ARMING_MODE))] = selector.selector(
        {
            "select": {
                "options": [
                    TAG_ACTION_ARM_HOME,
                    TAG_ACTION_ARM_AWAY,
                ],
                "translation_key": "tag_arming_mode",
            }
        }
    )

    return vol.Schema(schema_dict)


class HaAlarmProFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 2

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            user_input.setdefault(CONF_AUTHORIZED_TAGS, [])
            tags_value = user_input.get(CONF_AUTHORIZED_TAGS)
            if isinstance(tags_value, str):
                user_input[CONF_AUTHORIZED_TAGS] = [tags_value] if tags_value else []
            user_input.pop(CONF_NFC_TAG, None)
            lights_value = user_input.get(CONF_INDICATOR_LIGHT)
            if isinstance(lights_value, str):
                user_input[CONF_INDICATOR_LIGHT] = [
                    lights_value
                ] if lights_value else []
            elif lights_value is None:
                user_input[CONF_INDICATOR_LIGHT] = []
            return self.async_create_entry(title="HA Alarm Pro", data=user_input)

        audio_files = await self.hass.async_add_executor_job(
            _scan_audio_paths, self.hass
        )
        tags = await self.hass.async_add_executor_job(_load_tags, self.hass)

        schema = _build_schema({}, audio_files, tags)
        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return HaAlarmProOptionsFlow(config_entry)


class HaAlarmProOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, entry):
        self.entry = entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            user_input.setdefault(CONF_AUTHORIZED_TAGS, self.entry.options.get(CONF_AUTHORIZED_TAGS, self.entry.data.get(CONF_AUTHORIZED_TAGS, [])))
            tags_value = user_input.get(CONF_AUTHORIZED_TAGS)
            if isinstance(tags_value, str):
                user_input[CONF_AUTHORIZED_TAGS] = [tags_value] if tags_value else []
            user_input.pop(CONF_NFC_TAG, None)
            lights_value = user_input.get(CONF_INDICATOR_LIGHT)
            if isinstance(lights_value, str):
                user_input[CONF_INDICATOR_LIGHT] = [
                    lights_value
                ] if lights_value else []
            elif lights_value is None:
                user_input[CONF_INDICATOR_LIGHT] = []
            return self.async_create_entry(title="", data=user_input)

        audio_files = await self.hass.async_add_executor_job(
            _scan_audio_paths, self.hass
        )
        tags = await self.hass.async_add_executor_job(_load_tags, self.hass)

        data = {**self.entry.data, **self.entry.options}
        schema = _build_schema(data, audio_files, tags)
        return self.async_show_form(step_id="init", data_schema=schema)
