
from __future__ import annotations

import os
from typing import Any

from homeassistant.components.alarm_control_panel import (
    AlarmControlPanelEntity,
    AlarmControlPanelEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import StateType
from homeassistant.const import (
    STATE_ALARM_ARMED_AWAY,
    STATE_ALARM_ARMED_HOME,
    STATE_ALARM_ARMING,
    STATE_ALARM_DISARMED,
    STATE_ALARM_PENDING,
    STATE_ALARM_TRIGGERED,
)

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
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    async_add_entities([HaAlarmProEntity(hass, entry)])


class HaAlarmProEntity(AlarmControlPanelEntity, RestoreEntity):
    _attr_has_entity_name = True
    _attr_name = "HA Alarm Pro"
    _attr_unique_id = "ha_alarm_pro_main"
    _attr_supported_features = (
        AlarmControlPanelEntityFeature.ARM_AWAY
        | AlarmControlPanelEntityFeature.ARM_HOME
        | AlarmControlPanelEntityFeature.TRIGGER
    )

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self._state = STATE_ALARM_DISARMED
        self._unsubs: list = []

        self._cfg = entry.options or entry.data

        # listeners for custom bus events from controller
        self._unsubs.append(self.hass.bus.async_listen(f"{DOMAIN}_trigger", self._handle_trigger))
        self._unsubs.append(self.hass.bus.async_listen(f"{DOMAIN}_disarm_request", self._handle_disarm_request))
        self._unsubs.append(self.hass.bus.async_listen(f"{DOMAIN}_auto_disarm", self._handle_auto_disarm))

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(identifiers={(DOMAIN, "ha_alarm_pro")}, name="HA Alarm Pro")

    @property
    def state(self) -> StateType:
        return self._state

    async def async_added_to_hass(self) -> None:
        last = await self.async_get_last_state()
        if last:
            self._state = last.state or STATE_ALARM_DISARMED

    async def _blink_indicator(self, times: int = 2) -> None:
        light = self._cfg.get(CONF_INDICATOR_LIGHT)
        if not light:
            return
        for _ in range(times):
            await self.hass.services.async_call("light", "turn_on", {"entity_id": light, "brightness_pct": 100}, blocking=True)
            await self.hass.async_add_executor_job(lambda: None)
            await self.hass.async_create_task(self.hass.services.async_call("light", "turn_off", {"entity_id": light}))

    def _resolve_media(self, mp3: str) -> tuple[str, str]:
        """Return (media_content_id, media_content_type)."""
        if not mp3:
            return "", ""
        if mp3.startswith("media-source://"):
            return mp3, "music"
        if mp3.startswith("/local/") or mp3.startswith("/media/"):
            # deliver as media-source relative
            return mp3, "music"
        # fallback: assume /local path
        return mp3, "music"

    async def _play_siren(self) -> None:
        player = self._cfg.get(CONF_SIREN_PLAYER)
        mp3 = self._cfg.get(CONF_MP3_FILE)
        volume = self._cfg.get(CONF_SIREN_VOLUME, 1)
        if not player or not mp3:
            return
        await self.hass.services.async_call("media_player", "volume_set", {"entity_id": player, "volume_level": volume}, blocking=True)
        media_content_id, media_type = self._resolve_media(mp3)
        await self.hass.services.async_call(
            "media_player",
            "play_media",
            {
                "entity_id": player,
                "media_content_id": media_content_id,
                "media_content_type": "audio/mp3" if media_type == "music" else media_type,
            },
            blocking=False,
        )

    async def async_alarm_arm_home(self, code: str | None = None) -> None:
        self._state = STATE_ALARM_ARMING
        self.async_write_ha_state()
        await self._blink_indicator(2)
        delay = int(self._cfg.get(CONF_EXIT_DELAY, 30))
        await self.hass.async_add_executor_job(lambda: None)
        async def _finish(now):
            self._state = STATE_ALARM_ARMED_HOME
            self.async_write_ha_state()
        from homeassistant.helpers.event import async_call_later
        async_call_later(self.hass, delay, _finish)

    async def async_alarm_arm_away(self, code: str | None = None) -> None:
        await self.async_alarm_arm_home(code)
        self._state = STATE_ALARM_ARMING
        self.async_write_ha_state()
        from homeassistant.helpers.event import async_call_later
        delay = int(self._cfg.get(CONF_EXIT_DELAY, 30))
        async def _finish(now):
            self._state = STATE_ALARM_ARMED_AWAY
            self.async_write_ha_state()
        async_call_later(self.hass, delay, _finish)

    async def async_alarm_disarm(self, code: str | None = None) -> None:
        self._state = STATE_ALARM_DISARMED
        self.async_write_ha_state()

    async def async_alarm_trigger(self, code: str | None = None) -> None:
        self._state = STATE_ALARM_TRIGGERED
        self.async_write_ha_state()
        await self._play_siren()

    @callback
    async def _handle_trigger(self, event) -> None:
        if self._state in (STATE_ALARM_ARMED_HOME, STATE_ALARM_ARMED_AWAY):
            await self.async_alarm_trigger()

    @callback
    async def _handle_disarm_request(self, event) -> None:
        await self.async_alarm_disarm()

    @callback
    async def _handle_auto_disarm(self, event) -> None:
        await self.async_alarm_disarm()

    async def async_will_remove_from_hass(self) -> None:
        for u in self._unsubs:
            try:
                u()
            except Exception:
                pass
        self._unsubs = []
