from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Callable, Optional

from homeassistant.components.alarm_control_panel import (
    AlarmControlPanelEntity,
    AlarmControlPanelEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import (
    async_track_state_change_event,
    async_track_time_change,
)
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.entity import DeviceInfo

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
    STATE_DISARMED,
    STATE_EXIT_DELAY,
    STATE_ARMED_HOME,
    STATE_ARMED_AWAY,
    STATE_ENTRY_DELAY,
    STATE_TRIGGERED,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    entity = HAAlarmLitePanel(hass, entry)
    async_add_entities([entity])

    async def _get_entity_from_call(call):
        return entity

    async def svc_test_indicator(call):
        ent = await _get_entity_from_call(call)
        await ent._blink(call.data.get("color", "yellow"), int(call.data.get("times", 2)))

    async def svc_test_siren(call):
        ent = await _get_entity_from_call(call)
        times = int(call.data.get("times", 1))
        for _ in range(times):
            await ent._play_mp3()
            await asyncio.sleep(0.5)

    async def svc_arm_exit_delay(call):
        ent = await _get_entity_from_call(call)
        await ent.async_alarm_arm_away()

    async def svc_disarm(call):
        ent = await _get_entity_from_call(call)
        await ent.async_alarm_disarm()

    async def svc_trigger(call):
        ent = await _get_entity_from_call(call)
        await ent.async_alarm_trigger()

    async def svc_health_check(call):
        ent = await _get_entity_from_call(call)
        healthy, reasons = ent._compute_health()
        text = "✅ Health OK" if healthy else ("🟡 Warnungen:\n- " + "\n- ".join(reasons))
        await hass.services.async_call(
            "persistent_notification", "create",
            {"title": "HA Alarm Lite – Health Check", "message": text, "notification_id": "ha_alarm_lite_health"},
            blocking=False
        )

    hass.services.async_register(DOMAIN, "test_indicator", svc_test_indicator)
    hass.services.async_register(DOMAIN, "test_siren", svc_test_siren)
    hass.services.async_register(DOMAIN, "arm_exit_delay", svc_arm_exit_delay)
    hass.services.async_register(DOMAIN, "disarm", svc_disarm)
    hass.services.async_register(DOMAIN, "trigger_alarm", svc_trigger)
    hass.services.async_register(DOMAIN, "health_check", svc_health_check)

class HAAlarmLitePanel(AlarmControlPanelEntity, RestoreEntity):
    _attr_has_entity_name = True
    _attr_name = "HA Alarm Lite"
    _attr_translation_key = "panel"
    _attr_supported_features = (
        AlarmControlPanelEntityFeature.ARM_HOME
        | AlarmControlPanelEntityFeature.ARM_AWAY
        | AlarmControlPanelEntityFeature.TRIGGER
    )

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self._state = STATE_DISARMED
        self._exit_task: Optional[asyncio.Task] = None
        self._entry_task: Optional[asyncio.Task] = None
        self._listeners: list[Callable] = []
        self._unsub_tag = None
        self._auto_disarm_unsub = None
        self._lock = asyncio.Lock()
        self._last_tag_id: str | None = None
        self._last_tag_ts: datetime | None = None
        self._last_sensor_ts: datetime | None = None
        self._state_since: datetime = datetime.utcnow()
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._attr_unique_id)},
            name="HA Alarm Lite",
            manufacturer="HA Community",
            model="Lite v0.4",
        )

    @property
    def opts(self) -> dict[str, Any]:
        o = self.entry.options
        return {
            CONF_INDICATOR: o.get(CONF_INDICATOR),
            CONF_SIREN_PLAYER: o.get(CONF_SIREN_PLAYER),
            CONF_SIREN_VOLUME: o.get(CONF_SIREN_VOLUME, DEFAULT_SIREN_VOLUME),
            CONF_MP3_SOURCE: o.get(CONF_MP3_SOURCE),
            CONF_ENTRY_SENSORS: o.get(CONF_ENTRY_SENSORS, []),
            CONF_NFC_TAG_ID: (o.get(CONF_NFC_TAG_ID) or "").lower(),
            CONF_EXIT_DELAY: o.get(CONF_EXIT_DELAY, DEFAULT_EXIT_DELAY),
            CONF_ENTRY_DELAY: o.get(CONF_ENTRY_DELAY, DEFAULT_ENTRY_DELAY),
            CONF_ACCEPT_ANY_WHEN_TRIGGERED: o.get(CONF_ACCEPT_ANY_WHEN_TRIGGERED, True),
            CONF_AUTO_DISARM_TIME: o.get(CONF_AUTO_DISARM_TIME, DEFAULT_AUTO_DISARM_TIME),
        }

    @property
    def state(self) -> str:
        return self._state

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        healthy, reasons = self._compute_health()
        o = self.opts
        return {
            "state_since": self._state_since.isoformat(),
            "pending_exit": self._exit_task is not None,
            "pending_entry": self._entry_task is not None,
            "last_tag_id": self._last_tag_id,
            "last_tag_at": self._last_tag_ts.isoformat() if self._last_tag_ts else None,
            "last_sensor_at": self._last_sensor_ts.isoformat() if self._last_sensor_ts else None,
            "configured": self._is_configured(),
            "healthy": healthy,
            "health_reasons": reasons,
            "indicator_light": o[CONF_INDICATOR],
            "siren_player": o[CONF_SIREN_PLAYER],
            "siren_volume": o[CONF_SIREN_VOLUME],
            "mp3_source": o[CONF_MP3_SOURCE],
            "entry_sensors": o[CONF_ENTRY_SENSORS],
            "nfc_tag_id": o[CONF_NFC_TAG_ID],
            "exit_delay": o[CONF_EXIT_DELAY],
            "entry_delay": o[CONF_ENTRY_DELAY],
            "accept_any_when_triggered": o[CONF_ACCEPT_ANY_WHEN_TRIGGERED],
            "auto_disarm_time": o[CONF_AUTO_DISARM_TIME],
        }

    def _is_configured(self) -> bool:
        o = self.opts
        return bool(o[CONF_INDICATOR] and o[CONF_SIREN_PLAYER] and o[CONF_ENTRY_SENSORS])

    def _compute_health(self) -> tuple[bool, list[str]]:
        reasons: list[str] = []
        o = self.opts
        if not self._is_configured():
            reasons.append("Unvollständig konfiguriert (Licht/Player/Sensoren).")
        if o[CONF_SIREN_PLAYER]:
            st = self.hass.states.get(o[CONF_SIREN_PLAYER])
            if not st or st.state in ("unavailable", "unknown"):
                reasons.append(f"Player {o[CONF_SIREN_PLAYER]} ist unavailable/unknown.")
        if o[CONF_INDICATOR]:
            st = self.hass.states.get(o[CONF_INDICATOR])
            if not st or st.state in ("unavailable", "unknown"):
                reasons.append(f"Licht {o[CONF_INDICATOR]} ist unavailable/unknown.")
        if not o[CONF_MP3_SOURCE] or not str(o[CONF_MP3_SOURCE]).startswith("media-source://"):
            reasons.append("MP3-Pfad ungültig – nutze media-source://media_source/local/...")
        if self._last_sensor_ts:
            if datetime.utcnow() - self._last_sensor_ts > timedelta(hours=24):
                reasons.append("Kein Sensorevent in den letzten 24h erkannt.")
        healthy = len(reasons) == 0
        return healthy, reasons

    @callback
    def _set_state(self, new: str) -> None:
        if self._state != new:
            self._state = new
            self._state_since = datetime.utcnow()
            self.async_write_ha_state()
            _LOGGER.debug("Alarm state -> %s", new)

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        last = await self.async_get_last_state()
        if last and last.state in (
            STATE_DISARMED, STATE_ARMED_HOME, STATE_ARMED_AWAY, STATE_TRIGGERED
        ):
            self._state = last.state
            self._state_since = datetime.utcnow()
        self._setup_listeners()
        self._setup_auto_disarm()

    async def async_will_remove_from_hass(self) -> None:
        for unsub in self._listeners:
            try:
                unsub()
            except Exception:
                pass
        self._listeners.clear()
        if self._auto_disarm_unsub:
            self._auto_disarm_unsub()
            self._auto_disarm_unsub = None
        await self._cancel_task(self._exit_task)
        await self._cancel_task(self._entry_task)

    def _setup_listeners(self) -> None:
        sensors = self.opts[CONF_ENTRY_SENSORS] or []
        if sensors:
            unsub = async_track_state_change_event(self.hass, sensors, self._on_sensor_change)
            self._listeners.append(unsub)

        @callback
        def _tag_handler(event):
            tag_id = str(event.data.get("tag_id", "")).lower()
            self._last_tag_id = tag_id or None
            self._last_tag_ts = datetime.utcnow()
            self._on_tag_scanned(tag_id)
        self._unsub_tag = self.hass.bus.async_listen("tag_scanned", _tag_handler)
        self._listeners.append(self._unsub_tag)

    def _setup_auto_disarm(self) -> None:
        try:
            hh, mm, ss = (self.opts[CONF_AUTO_DISARM_TIME] or DEFAULT_AUTO_DISARM_TIME).split(":")
            hour, minute, second = int(hh), int(mm), int(ss)
        except Exception:
            hour, minute, second = 6, 0, 0

        @callback
        def _at_time(now):
            self.hass.async_create_task(self.async_alarm_disarm(code=None))

        if self._auto_disarm_unsub:
            self._auto_disarm_unsub()

        self._auto_disarm_unsub = async_track_time_change(
            self.hass, _at_time, hour=hour, minute=minute, second=second
        )

    @callback
    def _on_sensor_change(self, event):
        new_state = event.data.get("new_state")
        if new_state and new_state.state == "on":
            self._last_sensor_ts = datetime.utcnow()
            self.hass.async_create_task(self._maybe_start_entry())

    async def _maybe_start_entry(self):
        async with self._lock:
            if self._state in (STATE_ARMED_AWAY, STATE_ARMED_HOME) and not self._entry_task:
                self._entry_task = self.hass.async_create_task(self._entry_delay_flow())

    def _on_tag_scanned(self, tag_id: str) -> None:
        allowed = (self.opts[CONF_NFC_TAG_ID] or "").lower()
        if self._state in (STATE_ARMED_AWAY, STATE_ARMED_HOME, STATE_TRIGGERED):
            if tag_id == allowed or (self._state == STATE_TRIGGERED and self.opts[CONF_ACCEPT_ANY_WHEN_TRIGGERED]):
                self.hass.async_create_task(self.async_alarm_disarm(code=None))
                return
        if self._state == STATE_DISARMED and tag_id == allowed:
            if not self._exit_task:
                self._exit_task = self.hass.async_create_task(self._exit_delay_flow())

    async def _cancel_task(self, task: Optional[asyncio.Task]):
        if task and not task.done():
            task.cancel()
            try:
                await task
            except Exception:
                pass

    async def _blink(self, color: str, times: int, duration: float = 0.3):
        light = self.opts[CONF_INDICATOR]
        if not light:
            return
        try:
            for _ in range(times):
                await self.hass.services.async_call("light", "turn_on",
                    {"entity_id": light, "color_name": color, "brightness_pct": 100}, blocking=True)
                await asyncio.sleep(duration)
                await self.hass.services.async_call("light", "turn_off",
                    {"entity_id": light}, blocking=True)
                await asyncio.sleep(0.2)
        except Exception as e:
            _LOGGER.debug("Blink error: %s", e)

    async def _play_mp3(self):
        player = self.opts[CONF_SIREN_PLAYER]
        mp3 = self.opts[CONF_MP3_SOURCE]
        vol = float(self.opts[CONF_SIREN_VOLUME] or DEFAULT_SIREN_VOLUME)
        if not player or not mp3:
            return
        try:
            await self.hass.services.async_call("media_player","play_media",
                {"entity_id": player, "media_content_id": "https://cast.home-assistant.io/redirect",
                 "media_content_type": "audio/mp3", "metadata": {}}, blocking=True)
            await self.hass.services.async_call("media_player","volume_set",
                {"entity_id": player, "volume_level": vol}, blocking=True)
            await asyncio.sleep(0.5)
            await self.hass.services.async_call("media_player","play_media",
                {"entity_id": player, "media_content_id": mp3,
                 "media_content_type": "music", "metadata": {}}, blocking=True)
        except Exception as e:
            _LOGGER.warning("MP3 playback failed: %s", e)

    async def _exit_delay_flow(self):
        async with self._lock:
            if self._state != STATE_DISARMED:
                return
            self._set_state(STATE_EXIT_DELAY)
        try:
            await self._blink("yellow", 2)
            delay = int(self.opts[CONF_EXIT_DELAY] or DEFAULT_EXIT_DELAY)
            for _ in range(delay * 10):
                async with self._lock:
                    if self._state != STATE_EXIT_DELAY:
                        return
                await asyncio.sleep(0.1)
            async with self._lock:
                if self._state != STATE_EXIT_DELAY:
                    return
                self._set_state(STATE_ARMED_AWAY)
            await self._blink("blue", 2)
            await self._play_mp3()
        finally:
            self._exit_task = None

    async def _entry_delay_flow(self):
        async with self._lock:
            if self._state in (STATE_ENTRY_DELAY, STATE_TRIGGERED):
                return
            if self._state not in (STATE_ARMED_AWAY, STATE_ARMED_HOME):
                return
            self._set_state(STATE_ENTRY_DELAY)
        try:
            await self._blink("orange", 1)
            delay = int(self.opts[CONF_ENTRY_DELAY] or DEFAULT_ENTRY_DELAY)
            for _ in range(delay * 10):
                async with self._lock:
                    if self._state == STATE_DISARMED:
                        return
                await asyncio.sleep(0.1)
            async with self._lock:
                if self._state == STATE_DISARMED:
                    return
                self._set_state(STATE_TRIGGERED)
            for _ in range(15):
                async with self._lock:
                    if self._state != STATE_TRIGGERED:
                        break
                await self._play_mp3()
                await self._blink("red", 1, duration=1.0)
                await asyncio.sleep(1.0)
        finally:
            self._entry_task = None

    async def async_alarm_disarm(self, code: str | None = None) -> None:
        async with self._lock:
            await self._cancel_task(self._exit_task)
            await self._cancel_task(self._entry_task)
            self._exit_task = None
            self._entry_task = None
            player = self.opts[CONF_SIREN_PLAYER]
            if player:
                try:
                    await self.hass.services.async_call("media_player","media_stop",
                        {"entity_id": player}, blocking=False)
                except Exception:
                    pass
            self._set_state(STATE_DISARMED)

    async def async_alarm_arm_home(self, code: str | None = None) -> None:
        async with self._lock:
            await self._cancel_task(self._exit_task)
            await self._cancel_task(self._entry_task)
            self._exit_task = None
            self._entry_task = None
            self._set_state(STATE_ARMED_HOME)

    async def async_alarm_arm_away(self, code: str | None = None) -> None:
        if not self._exit_task:
            self._exit_task = self.hass.async_create_task(self._exit_delay_flow())

    async def async_alarm_trigger(self, code: str | None = None) -> None:
        async with self._lock:
            await self._cancel_task(self._exit_task)
            await self._cancel_task(self._entry_task)
            self._exit_task = None
            self._entry_task = None
            self._set_state(STATE_TRIGGERED)