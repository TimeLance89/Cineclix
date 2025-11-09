
from __future__ import annotations

from typing import Any, Optional

from homeassistant.components.alarm_control_panel import (
    AlarmControlPanelEntity,
    AlarmControlPanelEntityFeature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from . import AlarmController


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    ctrl: AlarmController = hass.data[DOMAIN][entry.entry_id]
    name = entry.title or "HA Alarm Pro"
    async_add_entities([HAAlarmProEntity(ctrl, name)])


class HAAlarmProEntity(AlarmControlPanelEntity, RestoreEntity):
    _attr_has_entity_name = True
    _attr_name = "Alarm"
    _attr_supported_features = (
        AlarmControlPanelEntityFeature.ARM_AWAY
        | AlarmControlPanelEntityFeature.ARM_HOME
    )

    def __init__(self, controller: AlarmController, name: str) -> None:
        self._controller = controller
        self._attr_unique_id = f"{controller.entry_id}_alarm"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, controller.entry_id)},
            "name": name,
            "manufacturer": "HA Alarm Pro",
            "model": "Software",
        }

    @property
    def state(self) -> str | None:
        if self._controller.triggered:
            return "triggered"
        if self._controller.pending:
            return "pending"
        return "armed_away" if self._controller.armed else "disarmed"

    async def async_alarm_disarm(self, code: Optional[str] = None) -> None:
        await self._controller.async_disarm(source="entity")
        self.async_write_ha_state()

    async def async_alarm_arm_home(self, code: Optional[str] = None) -> None:
        await self._controller.async_arm()
        self.async_write_ha_state()

    async def async_alarm_arm_away(self, code: Optional[str] = None) -> None:
        await self._controller.async_arm()
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        state = await self.async_get_last_state()
        if state:
            if state.state == "armed_away":
                self._controller.armed = True
            elif state.state == "triggered":
                self._controller.triggered = True
            else:
                self._controller.armed = False
                self._controller.triggered = False
