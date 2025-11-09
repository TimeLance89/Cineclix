from __future__ import annotations

from typing import Optional

from homeassistant.components.alarm_control_panel import (
    AlarmControlPanelEntity,
    AlarmControlPanelEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, DATA_CTRL


# --- HA Alarm Lite: tolerant media normalization (v0.5.2) ---
def _normalize_media(uri: str | None) -> str | None:
    """Return a media-source compatible URI or None.
    Accepts:
      - media-source://... (passes through)
      - /media/... or media/...
      - /local/... or local/...   (/config/www)
      - http(s)://... (passes through)
    """
    if not uri:
        return None
    u = str(uri).strip()
    if u.startswith("media-source://"):
        return u
    if u.startswith("/media/"):
        return "media-source://media_source" + u
    if u.startswith("media/"):
        return "media-source://media_source/" + u
    if u.startswith("/local/"):
        return "media-source://media_source" + u
    if u.startswith("local/"):
        return "media-source://media_source/" + u
    if u.startswith("http://") or u.startswith("https://"):
        return u
    # Unknown pattern → be graceful: no siren instead of setup failure
    return None
# --- end normalization helper ---


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    ctrl = data[DATA_CTRL]
    entity = AlarmLitePanel(hass, entry, ctrl)
    async_add_entities([entity])


class AlarmLitePanel(AlarmControlPanelEntity):
    _attr_name = "HA Alarm Lite"
    _attr_unique_id = "ha_alarm_lite_panel"
    _attr_supported_features = (
        AlarmControlPanelEntityFeature.ARM_AWAY
        | AlarmControlPanelEntityFeature.TRIGGER
        | AlarmControlPanelEntityFeature.ARM_HOME
        | AlarmControlPanelEntityFeature.DISARM
    )

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, ctrl) -> None:
        self.hass = hass
        self._entry = entry
        self._ctrl = ctrl
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="HA Alarm Lite",
            manufacturer="HA Alarm Lite",
        )

    @property
    def state(self) -> str:
        # map controller states to alarm_control_panel states
        st = getattr(self._ctrl, "_state", "disarmed")
        if st == "arming":
            return "arming"
        if st == "armed":
            return "armed_away"
        if st == "triggered":
            return "triggered"
        if st == "pending":
            return "pending"
        return "disarmed"

    async def async_alarm_disarm(self, code: Optional[str] = None) -> None:
        await self._ctrl.async_disarm("panel")

    async def async_alarm_arm_home(self, code: Optional[str] = None) -> None:
        await self._ctrl.async_arm()

    async def async_alarm_arm_away(self, code: Optional[str] = None) -> None:
        await self._ctrl.async_arm()

    async def async_alarm_trigger(self, code: Optional[str] = None) -> None:
        await self._ctrl.async_trigger()