from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_NAME
from homeassistant.helpers import selector
from typing import Any

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

class AlarmLiteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            return self.async_create_entry(title=user_input.get(CONF_NAME, "HA Alarm Lite"), data={}, options=user_input)

        schema = vol.Schema({
            vol.Optional(CONF_NAME, default="HA Alarm Lite"): str,
            vol.Required(CONF_INDICATOR): selector.selector({"entity": {"domain": "light"}}),
            vol.Required(CONF_SIREN_PLAYER): selector.selector({"entity": {"domain": "media_player"}}),
            vol.Optional(CONF_SIREN_VOLUME, default=DEFAULT_SIREN_VOLUME): selector.selector({"number": {"min": 0, "max": 1, "step": 0.05}}),
            vol.Required(CONF_MP3_SOURCE): selector.selector({"text": {}}),
            vol.Required(CONF_ENTRY_SENSORS): selector.selector({"entity": {"domain": "binary_sensor", "multiple": True}}),
            vol.Required(CONF_NFC_TAG_ID): selector.selector({"text": {}}),
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

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        o = self.config_entry.options

        last_tag = ""
        entity_id = "alarm_control_panel.ha_alarm_lite"
        st = self.hass.states.get(entity_id)
        if st:
            last_tag = st.attributes.get("last_tag_id") or ""

        schema = vol.Schema({
            vol.Required(CONF_INDICATOR, default=o.get(CONF_INDICATOR)): selector.selector({"entity": {"domain": "light"}}),
            vol.Required(CONF_SIREN_PLAYER, default=o.get(CONF_SIREN_PLAYER)): selector.selector({"entity": {"domain": "media_player"}}),
            vol.Optional(CONF_SIREN_VOLUME, default=o.get(CONF_SIREN_VOLUME, DEFAULT_SIREN_VOLUME)): selector.selector({"number": {"min": 0, "max": 1, "step": 0.05}}),
            vol.Required(CONF_MP3_SOURCE, default=o.get(CONF_MP3_SOURCE, "")): selector.selector({"text": {}}),
            vol.Required(CONF_ENTRY_SENSORS, default=o.get(CONF_ENTRY_SENSORS, [])): selector.selector({"entity": {"domain": "binary_sensor", "multiple": True}}),
            vol.Required(CONF_NFC_TAG_ID, default=o.get(CONF_NFC_TAG_ID, last_tag)): selector.selector({"text": {}}),
            vol.Optional(CONF_EXIT_DELAY, default=o.get(CONF_EXIT_DELAY, DEFAULT_EXIT_DELAY)): selector.selector({"number": {"min": 0, "max": 600, "mode": "box"}}),
            vol.Optional(CONF_ENTRY_DELAY, default=o.get(CONF_ENTRY_DELAY, DEFAULT_ENTRY_DELAY)): selector.selector({"number": {"min": 0, "max": 600, "mode": "box"}}),
            vol.Optional(CONF_ACCEPT_ANY_WHEN_TRIGGERED, default=o.get(CONF_ACCEPT_ANY_WHEN_TRIGGERED, True)): selector.selector({"boolean": {}}),
            vol.Optional(CONF_AUTO_DISARM_TIME, default=o.get(CONF_AUTO_DISARM_TIME, DEFAULT_AUTO_DISARM_TIME)): selector.selector({"time": {}}),
        })

        return self.async_show_form(step_id="init", data_schema=schema)