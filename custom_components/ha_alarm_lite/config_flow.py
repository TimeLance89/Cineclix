from __future__ import annotations

import os
from typing import Any, Dict, List

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers import selector
from .const import (
    DOMAIN,
    CONF_INDICATOR_LIGHT,
    CONF_SIREN_PLAYER,
    CONF_SIREN_VOLUME,
    CONF_MP3_FILE,
    CONF_ENTRY_SENSORS,
    CONF_NFC_TAG,
    CONF_EXIT_DELAY,
    CONF_ENTRY_DELAY,
    CONF_ALLOW_ANY_TAG,
    CONF_AUTO_DISARM_TIME,
)

async def _discover_mp3s(hass: HomeAssistant) -> List[str]:
    mp3s: List[str] = []
    # /media
    media_root = hass.config.media_dirs.get("media")
    if media_root and os.path.isdir(media_root):
        for root, _, files in await hass.async_add_executor_job(lambda: list(os.walk(media_root))):
            for f in files:
                if f.lower().endswith(".mp3"):
                    rel = os.path.relpath(os.path.join(root, f), media_root).replace("\\", "/")
                    mp3s.append(f"media/{rel}")
    # /config/www -> /local
    www_root = hass.config.path("www")
    if os.path.isdir(www_root):
        for root, _, files in await hass.async_add_executor_job(lambda: list(os.walk(www_root))):
            for f in files:
                if f.lower().endswith(".mp3"):
                    rel = os.path.relpath(os.path.join(root, f), www_root).replace("\\", "/")
                    mp3s.append(f"/local/{rel}")
    return sorted(dict.fromkeys(mp3s))

async def _list_tags(hass: HomeAssistant) -> Dict[str, str]:
    try:
        from homeassistant.components.tag import async_get_registry  # type: ignore
    except Exception:
        return {}

    reg = await async_get_registry(hass)
    result: Dict[str, str] = {}
    for tag in reg.tags.values():
        label = tag.name or tag.id
        result[tag.id] = label
    return result

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: Dict[str, Any] | None = None):
        errors: Dict[str, str] = {}
        if user_input is not None:
            return self.async_create_entry(title="HA Alarm Lite", data={}, options=user_input)

        mp3s = await _discover_mp3s(self.hass)
        tags = await _list_tags(self.hass)

        data_schema = vol.Schema({
            vol.Optional(CONF_INDICATOR_LIGHT): selector.selector({
                "entity": {"domain": "light"}
            }),
            vol.Required(CONF_SIREN_PLAYER): selector.selector({
                "entity": {"domain": "media_player"}
            }),
            vol.Required(CONF_SIREN_VOLUME, default=1): selector.selector({
                "number": {"min": 0, "max": 1, "step": 0.05, "mode": "slider"}
            }),
            vol.Required(CONF_MP3_FILE): selector.selector({
                "select": {"options": mp3s} if mp3s else {"options": []}
            }),
            vol.Required(CONF_ENTRY_SENSORS): selector.selector({
                "entity": {"domain": "binary_sensor", "multiple": True}
            }),
            vol.Optional(CONF_NFC_TAG): selector.selector({
                "select": {"options": [{"label": v, "value": k} for k, v in tags.items()]}
            }),
            vol.Required(CONF_EXIT_DELAY, default=30): selector.selector({"number": {"min": 0, "max": 600}}),
            vol.Required(CONF_ENTRY_DELAY, default=30): selector.selector({"number": {"min": 0, "max": 600}}),
            vol.Optional(CONF_ALLOW_ANY_TAG, default=False): selector.selector({"boolean": {}}),
            vol.Optional(CONF_AUTO_DISARM_TIME): selector.selector({"time": {}}),
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    async def async_step_finish(self, user_input: Dict[str, Any] | None = None):
        return self.async_show_form(step_id="finish")

    async def async_get_options_flow(self, entry):
        return OptionsFlow(entry)


class OptionsFlow(config_entries.OptionsFlow):
    def __init__(self, entry: config_entries.ConfigEntry) -> None:
        self.entry = entry

    async def async_step_init(self, user_input: Dict[str, Any] | None = None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        mp3s = await _discover_mp3s(self.hass)
        tags = await _list_tags(self.hass)

        opts = {**self.entry.options}
        data_schema = vol.Schema({
            vol.Optional(CONF_INDICATOR_LIGHT, default=opts.get(CONF_INDICATOR_LIGHT)): selector.selector({
                "entity": {"domain": "light"}
            }),
            vol.Optional(CONF_SIREN_PLAYER, default=opts.get(CONF_SIREN_PLAYER)): selector.selector({
                "entity": {"domain": "media_player"}
            }),
            vol.Optional(CONF_SIREN_VOLUME, default=opts.get(CONF_SIREN_VOLUME, 1)): selector.selector({
                "number": {"min": 0, "max": 1, "step": 0.05, "mode": "slider"}
            }),
            vol.Optional(CONF_MP3_FILE, default=opts.get(CONF_MP3_FILE)): selector.selector({
                "select": {"options": mp3s} if mp3s else {"options": []}
            }),
            vol.Optional(CONF_ENTRY_SENSORS, default=opts.get(CONF_ENTRY_SENSORS)): selector.selector({
                "entity": {"domain": "binary_sensor", "multiple": True}
            }),
            vol.Optional(CONF_NFC_TAG, default=opts.get(CONF_NFC_TAG)): selector.selector({
                "select": {"options": [{"label": v, "value": k} for k, v in tags.items()]}
            }),
            vol.Optional(CONF_EXIT_DELAY, default=opts.get(CONF_EXIT_DELAY, 30)): selector.selector({"number": {"min": 0, "max": 600}}),
            vol.Optional(CONF_ENTRY_DELAY, default=opts.get(CONF_ENTRY_DELAY, 30)): selector.selector({"number": {"min": 0, "max": 600}}),
            vol.Optional(CONF_ALLOW_ANY_TAG, default=opts.get(CONF_ALLOW_ANY_TAG, False)): selector.selector({"boolean": {}}),
            vol.Optional(CONF_AUTO_DISARM_TIME, default=opts.get(CONF_AUTO_DISARM_TIME)): selector.selector({"time": {}}),
        })

        return self.async_show_form(step_id="init", data_schema=data_schema)
