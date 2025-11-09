
from __future__ import annotations

import os
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback, HomeAssistant
from homeassistant.const import CONF_NAME
from homeassistant.helpers.selector import (
    EntitySelector, EntitySelectorConfig,
    NumberSelector, NumberSelectorConfig,
    NumberSelectorMode,
    TimeSelector, BooleanSelector
)
from homeassistant.helpers import entity_registry as er

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    CONF_INDICATOR,
    CONF_MEDIA_PLAYER,
    CONF_VOLUME,
    CONF_MP3,
    CONF_SENSORS,
    CONF_EXIT_DELAY,
    CONF_ENTRY_DELAY,
    CONF_ALLOW_ANY_TAG,
    CONF_NFC_TAG,
    CONF_AUTO_DISARM,
)

MEDIA_DIRS = ("media", "www", "config/www", "local")

def _list_mp3(hass: HomeAssistant) -> list[str]:
    results: list[str] = []
    base = hass.config.path("")
    for d in MEDIA_DIRS:
        absd = hass.config.path(d)
        if not os.path.isdir(absd):
            continue
        for root, _dirs, files in os.walk(absd):
            for f in files:
                if f.lower().endswith(".mp3"):
                    rel = os.path.relpath(os.path.join(root, f), base).replace("\\", "/")
                    # normalize to media-source friendly
                    if rel.startswith("www/"):
                        results.append("local/" + rel.split("www/",1)[1])
                    elif rel.startswith("config/www/"):
                        results.append("local/" + rel.split("config/www/",1)[1])
                    else:
                        results.append(rel)
    # unique
    return sorted(dict.fromkeys(results))

def _list_tags(hass: HomeAssistant) -> list[str]:
    try:
        path = hass.config.path(".storage/tag")
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [item.get("id") for item in data.get("items", []) if item.get("id")]
    except Exception:  # noqa: BLE001
        return []


class HAAlarmProConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: Dict[str, Any] | None = None):
        if user_input is not None:
            title = user_input.get(CONF_NAME, DEFAULT_NAME)
            return self.async_create_entry(title=title, data=user_input)

        er_select = EntitySelector(EntitySelectorConfig(domain="light"))
        mp_select = EntitySelector(EntitySelectorConfig(domain="media_player"))
        bs_select = EntitySelector(EntitySelectorConfig(domain="binary_sensor"))
        mp3s = await self.hass.async_add_executor_job(_list_mp3, self.hass)
        tags = await self.hass.async_add_executor_job(_list_tags, self.hass)

        schema = vol.Schema({
            vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
            vol.Optional(CONF_INDICATOR): er_select,
            vol.Optional(CONF_MEDIA_PLAYER): mp_select,
            vol.Optional(CONF_VOLUME, default=1.0): NumberSelector(NumberSelectorConfig(min=0, max=1, step=0.05, mode=NumberSelectorMode.SLIDER)),
            vol.Optional(CONF_MP3): vol.In(mp3s) if mp3s else str,
            vol.Optional(CONF_SENSORS): bs_select,
            vol.Optional(CONF_EXIT_DELAY, default=30): NumberSelector(NumberSelectorConfig(min=0, max=300, step=1, mode=NumberSelectorMode.SLIDER)),
            vol.Optional(CONF_ENTRY_DELAY, default=30): NumberSelector(NumberSelectorConfig(min=0, max=300, step=1, mode=NumberSelectorMode.SLIDER)),
            vol.Optional(CONF_ALLOW_ANY_TAG, default=False): BooleanSelector(),
            vol.Optional(CONF_NFC_TAG): vol.In(tags) if tags else str,
            vol.Optional(CONF_AUTO_DISARM): TimeSelector(),
        })
        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return HAAlarmProOptionsFlow(config_entry)


class HAAlarmProOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, entry):
        self.entry = entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            data = {**self.entry.data, **user_input}
            self.hass.config_entries.async_update_entry(self.entry, data=data)
            return self.async_create_entry(title="", data={})

        mp3s = await self.hass.async_add_executor_job(_list_mp3, self.hass)
        tags = await self.hass.async_add_executor_job(_list_tags, self.hass)

        er_select = EntitySelector(EntitySelectorConfig(domain="light"))
        mp_select = EntitySelector(EntitySelectorConfig(domain="media_player"))
        bs_select = EntitySelector(EntitySelectorConfig(domain="binary_sensor"))

        data = self.entry.data
        schema = vol.Schema({
            vol.Optional(CONF_INDICATOR, default=data.get(CONF_INDICATOR)): er_select,
            vol.Optional(CONF_MEDIA_PLAYER, default=data.get(CONF_MEDIA_PLAYER)): mp_select,
            vol.Optional(CONF_VOLUME, default=data.get(CONF_VOLUME, 1.0)): NumberSelector(NumberSelectorConfig(min=0, max=1, step=0.05, mode=NumberSelectorMode.SLIDER)),
            vol.Optional(CONF_MP3, default=data.get(CONF_MP3)): vol.In(mp3s) if mp3s else str,
            vol.Optional(CONF_SENSORS, default=data.get(CONF_SENSORS)): bs_select,
            vol.Optional(CONF_EXIT_DELAY, default=data.get(CONF_EXIT_DELAY,30)): NumberSelector(NumberSelectorConfig(min=0, max=300, step=1, mode=NumberSelectorMode.SLIDER)),
            vol.Optional(CONF_ENTRY_DELAY, default=data.get(CONF_ENTRY_DELAY,30)): NumberSelector(NumberSelectorConfig(min=0, max=300, step=1, mode=NumberSelectorMode.SLIDER)),
            vol.Optional(CONF_ALLOW_ANY_TAG, default=data.get(CONF_ALLOW_ANY_TAG, False)): BooleanSelector(),
            vol.Optional(CONF_NFC_TAG, default=data.get(CONF_NFC_TAG)): vol.In(tags) if tags else str,
            vol.Optional(CONF_AUTO_DISARM, default=data.get(CONF_AUTO_DISARM)): TimeSelector(),
        })
        return self.async_show_form(step_id="init", data_schema=schema)
