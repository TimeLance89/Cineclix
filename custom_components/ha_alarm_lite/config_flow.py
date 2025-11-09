from __future__ import annotations

import os
from typing import Any, List
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.selector import selector

from .const import DOMAIN


def _default(options: dict, key: str, fallback: Any = None) -> Any:
    return options.get(key, fallback)


class HAAlarmLiteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None):
        if user_input is not None:
            title = user_input.get("name", "HA Alarm Lite")
            return self.async_create_entry(title=title, data={})

        schema = vol.Schema({
            vol.Required("name", default="HA Alarm Lite"): str,
        })
        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, entry: config_entries.ConfigEntry) -> None:
        self.entry = entry

    async def async_step_init(self, user_input: dict | None = None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        opts = dict(self.entry.options)

        # Discover MP3s
        mp3_choices = await self._async_find_mp3s(self.hass)
        nfc_choices = await self._async_list_nfc_tags(self.hass)

        schema = vol.Schema({
            vol.Optional("indicator_entity", default=_default(opts, "indicator_entity")): selector({"entity": {"domain": "light"}}),
            vol.Optional("siren_entity", default=_default(opts, "siren_entity")): selector({"entity": {"domain": "media_player"}}),
            vol.Optional("siren_volume", default=_default(opts, "siren_volume", 1.0)): vol.All(vol.Coerce(float), vol.Range(min=0.0, max=1.0)),
            vol.Optional("mp3_path", default=_default(opts, "mp3_path", "")): selector({"select": {"options": mp3_choices}}) if mp3_choices else str,
            vol.Optional("entry_sensors", default=_default(opts, "entry_sensors", [])): selector({"entity": {"domain": "binary_sensor", "multiple": True}}),
            vol.Optional("nfc_tag", default=_default(opts, "nfc_tag", "")): selector({"select": {"options": nfc_choices}}) if nfc_choices else str,
            vol.Optional("exit_delay", default=_default(opts, "exit_delay", 30)): vol.Coerce(int),
            vol.Optional("entry_delay", default=_default(opts, "entry_delay", 30)): vol.Coerce(int),
            vol.Optional("any_tag_can_disarm", default=_default(opts, "any_tag_can_disarm", False)): selector({"boolean": {}}),
            vol.Optional("auto_disarm_time", default=_default(opts, "auto_disarm_time")): selector({"time": {}}),
        })

        return self.async_show_form(step_id="init", data_schema=schema, description_placeholders={})

    async def _async_find_mp3s(self, hass: HomeAssistant) -> List[str]:
        base_cfg = hass.config.path("")
        paths = [hass.config.path("www"), hass.config.path("media")]
        results: List[str] = []
        for base in paths:
            try:
                for root, _dirs, files in os.walk(base):
                    for f in files:
                        if f.lower().endswith(".mp3"):
                            rel = os.path.relpath(os.path.join(root, f), start=base_cfg).replace("\\", "/")
                            # Prefer 'media/...' or 'www/...'
                            results.append(rel)
            except Exception:  # pragma: no cover - best-effort
                continue
        # unique & sorted
        uniq = sorted(dict.fromkeys(results).keys())
        return uniq

    async def _async_list_nfc_tags(self, hass: HomeAssistant) -> List[str]:
        try:
            from homeassistant.components.tag import async_get_registry
            reg = await async_get_registry(hass)
            # registry.async_list() returns list[dict] with 'id'
            return sorted([t["id"] for t in reg.async_list()])
        except Exception:  # fall back to manual entry
            return []
