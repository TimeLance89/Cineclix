
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
    CONF_ENTRY_SENSORS,
    CONF_NFC_TAG,
    CONF_ALLOW_ANY_TAG,
    CONF_EXIT_DELAY,
    CONF_ENTRY_DELAY,
    CONF_AUTO_DISARM_TIME,
    DEFAULT_ENTRY_DELAY,
    DEFAULT_EXIT_DELAY,
    DEFAULT_VOLUME,
)


def _scan_mp3_paths(hass: HomeAssistant) -> list[str]:
    res: list[str] = []
    # /media
    media_path = hass.config.path("media")
    www_path = hass.config.path("www")
    try:
        for base, prefix in [(media_path, "/media/"), (www_path, "/local/")]:
            if os.path.isdir(base):
                for root, _, files in os.walk(base):
                    for f in files:
                        if f.lower().endswith(".mp3"):
                            full = os.path.join(root, f)
                            rel = prefix + os.path.relpath(full, base).replace("\\", "/")
                            res.append(rel)
    except Exception:
        pass
    return sorted(res)

def _load_tags(hass: HomeAssistant) -> list[tuple[str,str]]:
    # returns list of (id, name_or_id)
    tags_file = hass.config.path(".storage", "tag")
    out: list[tuple[str,str]] = []
    try:
        with open(tags_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data.get("data", []):
                tid = item.get("id")
                name = item.get("name") or tid
                if tid:
                    out.append((tid, name))
    except Exception:
        pass
    return out


class HaAlarmProFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            return self.async_create_entry(title="HA Alarm Pro", data=user_input)

        mp3s = await self.hass.async_add_executor_job(_scan_mp3_paths, self.hass)
        tags = await self.hass.async_add_executor_job(_load_tags, self.hass)

        schema_dict: dict[Any, Any] = {}
        schema_dict[vol.Optional(CONF_INDICATOR_LIGHT)] = selector.selector({"entity": {"domain": "light"}})
        schema_dict[vol.Optional(CONF_SIREN_PLAYER)] = selector.selector({"entity": {"domain": "media_player"}})
        schema_dict[vol.Required(CONF_SIREN_VOLUME, default=DEFAULT_VOLUME)] = selector.selector({"number": {"min": 0, "max": 1, "step": 0.05, "mode": "slider"}})

        mp3_key = vol.Optional(CONF_MP3_FILE)
        mp3_selector_config: dict[str, Any] = {"text": {}}
        if mp3s:
            mp3_selector_config = {"select": {"options": mp3s, "custom_value": True}}
        else:
            mp3_key = vol.Optional(CONF_MP3_FILE, default="")
        schema_dict[mp3_key] = selector.selector(mp3_selector_config)

        schema_dict[vol.Required(CONF_ENTRY_SENSORS)] = selector.selector({"entity": {"domain": "binary_sensor", "multiple": True}})

        tag_key = vol.Optional(CONF_NFC_TAG)
        tag_selector_config: dict[str, Any] = {"text": {}}
        if tags:
            tag_selector_config = {"select": {"options": [t[0] for t in tags], "custom_value": True}}
        else:
            tag_key = vol.Optional(CONF_NFC_TAG, default="")
        schema_dict[tag_key] = selector.selector(tag_selector_config)

        schema_dict[vol.Required(CONF_ALLOW_ANY_TAG, default=False)] = selector.selector({"boolean": {}})
        schema_dict[vol.Required(CONF_EXIT_DELAY, default=DEFAULT_EXIT_DELAY)] = selector.selector({"number": {"min": 0, "max": 300, "mode": "box"}})
        schema_dict[vol.Required(CONF_ENTRY_DELAY, default=DEFAULT_ENTRY_DELAY)] = selector.selector({"number": {"min": 0, "max": 300, "mode": "box"}})
        schema_dict[vol.Optional(CONF_AUTO_DISARM_TIME)] = selector.selector({"time": {}})

        schema = vol.Schema(schema_dict)
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
            return self.async_create_entry(title="", data=user_input)

        mp3s = await self.hass.async_add_executor_job(_scan_mp3_paths, self.hass)
        tags = await self.hass.async_add_executor_job(_load_tags, self.hass)

        data = {**self.entry.data, **self.entry.options}

        schema_dict: dict[Any, Any] = {}
        schema_dict[vol.Optional(CONF_INDICATOR_LIGHT, default=data.get(CONF_INDICATOR_LIGHT))] = selector.selector({"entity": {"domain": "light"}})
        schema_dict[vol.Optional(CONF_SIREN_PLAYER, default=data.get(CONF_SIREN_PLAYER))] = selector.selector({"entity": {"domain": "media_player"}})
        schema_dict[vol.Required(CONF_SIREN_VOLUME, default=data.get(CONF_SIREN_VOLUME, DEFAULT_VOLUME))] = selector.selector({"number": {"min": 0, "max": 1, "step": 0.05, "mode": "slider"}})

        mp3_default = data.get(CONF_MP3_FILE, "")
        mp3_key = vol.Optional(CONF_MP3_FILE, default=mp3_default)
        mp3_selector_config = {"text": {}}
        if mp3s:
            mp3_selector_config = {"select": {"options": mp3s, "custom_value": True}}
        schema_dict[mp3_key] = selector.selector(mp3_selector_config)

        schema_dict[vol.Optional(CONF_ENTRY_SENSORS, default=data.get(CONF_ENTRY_SENSORS))] = selector.selector({"entity": {"domain": "binary_sensor", "multiple": True}})

        tag_default = data.get(CONF_NFC_TAG, "")
        tag_key = vol.Optional(CONF_NFC_TAG, default=tag_default)
        tag_selector_config = {"text": {}}
        if tags:
            tag_selector_config = {"select": {"options": [t[0] for t in tags], "custom_value": True}}
        schema_dict[tag_key] = selector.selector(tag_selector_config)

        schema_dict[vol.Optional(CONF_ALLOW_ANY_TAG, default=data.get(CONF_ALLOW_ANY_TAG, False))] = selector.selector({"boolean": {}})
        schema_dict[vol.Optional(CONF_EXIT_DELAY, default=data.get(CONF_EXIT_DELAY, DEFAULT_EXIT_DELAY))] = selector.selector({"number": {"min": 0, "max": 300, "mode": "box"}})
        schema_dict[vol.Optional(CONF_ENTRY_DELAY, default=data.get(CONF_ENTRY_DELAY, DEFAULT_ENTRY_DELAY))] = selector.selector({"number": {"min": 0, "max": 300, "mode": "box"}})
        schema_dict[vol.Optional(CONF_AUTO_DISARM_TIME, default=data.get(CONF_AUTO_DISARM_TIME))] = selector.selector({"time": {}})

        schema = vol.Schema(schema_dict)
        return self.async_show_form(step_id="init", data_schema=schema)
