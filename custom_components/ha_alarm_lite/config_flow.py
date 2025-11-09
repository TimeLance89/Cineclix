from __future__ import annotations

from typing import Any, List, Dict
import os
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_INDICATOR,
    CONF_SIREN_PLAYER,
    CONF_SIREN_VOLUME,
    CONF_MP3_SOURCE,
    CONF_ENTRY_SENSORS,
    CONF_NFC_TAG_ID,
    CONF_EXIT_DELAY,
    CONF_ENTRY_DELAY,
    CONF_ACCEPT_ANY_WHEN_TRIGGERED,
    CONF_AUTO_DISARM_TIME,
    DEFAULT_EXIT_DELAY,
    DEFAULT_ENTRY_DELAY,
    DEFAULT_SIREN_VOLUME,
    DEFAULT_AUTO_DISARM_TIME,
)


def _normalize_media_source(path: str) -> str:
    """Accept raw file paths and convert to media-source://."""
    if not path:
        return path
    p = str(path).strip().replace("\\", "/")
    if p.startswith("media-source://"):
        return p
    # map /config/www and www/ to local media_source
    if "/www/" in p or p.startswith("www/") or p.startswith("/config/www/"):
        rel = p.split("/www/", 1)[1] if "/www/" in p else p.split("www/", 1)[1]
        return f"media-source://media_source/local/{rel}"
    # map /media to media_source
    if p.startswith("/media/") or p.startswith("media/"):
        rel = p.split("/media/", 1)[1] if "/media/" in p else p.split("media/", 1)[1]
        return f"media-source://media_source/{rel}"
    return p


def _discover_mp3s(hass) -> List[Dict[str, str]]:
    """Find .mp3 under /media and /config/www, return select options with label/value."""
    options: List[Dict[str, str]] = []
    roots = [
        (hass.config.path("www"), "local"),
        (hass.config.path("media"), "media"),
    ]
    for root, kind in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, _dirnames, filenames in os.walk(root):
            for fn in filenames:
                if not fn.lower().endswith(".mp3"):
                    continue
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, root).replace("\\", "/")
                if kind == "local":
                    uri = f"media-source://media_source/local/{rel}"
                    label = f"www/{rel}"
                else:
                    uri = f"media-source://media_source/{rel}"
                    label = f"media/{rel}"
                options.append({"label": label, "value": uri})
    options.sort(key=lambda x: x["label"].lower())
    return options


async def _discover_tags(hass) -> List[Dict[str, str]]:
    """Read Tag registry and offer id + friendly name."""
    options: List[Dict[str, str]] = []
    try:
        from homeassistant.components.tag import async_get_registry  # type: ignore
        registry = await async_get_registry(hass)
        tags = await registry.async_list()  # returns list of TagEntry
        for t in tags:
            tag_id = getattr(t, "tag_id", None) or getattr(t, "id", None)
            name = getattr(t, "name", None) or tag_id
            if not tag_id:
                continue
            label = f"{name} ({tag_id})" if name and name != tag_id else tag_id
            options.append({"label": label, "value": tag_id})
    except Exception:  # pragma: no cover - fallback if API changes
        pass
    options.sort(key=lambda x: x["label"].lower())
    return options


class AlarmLiteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            if user_input.get(CONF_MP3_SOURCE):
                user_input[CONF_MP3_SOURCE] = _normalize_media_source(user_input[CONF_MP3_SOURCE])
            return self.async_create_entry(
                title="HA Alarm Lite",
                data={},
                options=user_input,
            )

        mp3_options = _discover_mp3s(self.hass)
        tag_options = await _discover_tags(self.hass)

        schema = vol.Schema({
            vol.Required(CONF_INDICATOR): selector.selector({"entity": {"domain": "light"}}),
            vol.Required(CONF_SIREN_PLAYER): selector.selector({"entity": {"domain": "media_player"}}),
            vol.Optional(CONF_SIREN_VOLUME, default=DEFAULT_SIREN_VOLUME): selector.selector({"number": {"min": 0, "max": 1, "step": 0.05}}),
            vol.Required(CONF_MP3_SOURCE): selector.selector({"select": {"options": mp3_options, "custom_value": True}}),
            vol.Required(CONF_ENTRY_SENSORS): selector.selector({"entity": {"domain": "binary_sensor", "multiple": True}}),
            vol.Required(CONF_NFC_TAG_ID): selector.selector({"select": {"options": tag_options, "custom_value": True}}),
            vol.Optional(CONF_EXIT_DELAY, default=DEFAULT_EXIT_DELAY): selector.selector({"number": {"min": 0, "max": 600, "mode": "box"}}),
            vol.Optional(CONF_ENTRY_DELAY, default=DEFAULT_ENTRY_DELAY): selector.selector({"number": {"min": 0, "max": 600, "mode": "box"}}),
            vol.Optional(CONF_ACCEPT_ANY_WHEN_TRIGGERED, default=True): selector.selector({"boolean": {}}),
            vol.Optional(CONF_AUTO_DISARM_TIME, default=DEFAULT_AUTO_DISARM_TIME): selector.selector({"time": {}}),
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return AlarmLiteOptionsFlow(config_entry)


class AlarmLiteOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            if user_input.get(CONF_MP3_SOURCE):
                user_input[CONF_MP3_SOURCE] = _normalize_media_source(user_input[CONF_MP3_SOURCE])
            return self.async_create_entry(title="", data=user_input)

        o = self.config_entry.options
        mp3_options = _discover_mp3s(self.hass)
        tag_options = await _discover_tags(self.hass)

        schema = vol.Schema({
            vol.Required(CONF_INDICATOR, default=o.get(CONF_INDICATOR)): selector.selector({"entity": {"domain": "light"}}),
            vol.Required(CONF_SIREN_PLAYER, default=o.get(CONF_SIREN_PLAYER)): selector.selector({"entity": {"domain": "media_player"}}),
            vol.Optional(CONF_SIREN_VOLUME, default=o.get(CONF_SIREN_VOLUME, DEFAULT_SIREN_VOLUME)): selector.selector({"number": {"min": 0, "max": 1, "step": 0.05}}),
            vol.Required(CONF_MP3_SOURCE, default=o.get(CONF_MP3_SOURCE, "")): selector.selector({"select": {"options": mp3_options, "custom_value": True}}),
            vol.Required(CONF_ENTRY_SENSORS, default=o.get(CONF_ENTRY_SENSORS, [])): selector.selector({"entity": {"domain": "binary_sensor", "multiple": True}}),
            vol.Required(CONF_NFC_TAG_ID, default=o.get(CONF_NFC_TAG_ID, "")): selector.selector({"select": {"options": tag_options, "custom_value": True}}),
            vol.Optional(CONF_EXIT_DELAY, default=o.get(CONF_EXIT_DELAY, DEFAULT_EXIT_DELAY)): selector.selector({"number": {"min": 0, "max": 600, "mode": "box"}}),
            vol.Optional(CONF_ENTRY_DELAY, default=o.get(CONF_ENTRY_DELAY, DEFAULT_ENTRY_DELAY)): selector.selector({"number": {"min": 0, "max": 600, "mode": "box"}}),
            vol.Optional(CONF_ACCEPT_ANY_WHEN_TRIGGERED, default=o.get(CONF_ACCEPT_ANY_WHEN_TRIGGERED, True)): selector.selector({"boolean": {}}),
            vol.Optional(CONF_AUTO_DISARM_TIME, default=o.get(CONF_AUTO_DISARM_TIME, DEFAULT_AUTO_DISARM_TIME)): selector.selector({"time": {}}),
        })

        return self.async_show_form(step_id="init", data_schema=schema)
