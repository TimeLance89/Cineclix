from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, time
from typing import Any, Dict, List, Optional

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import storage
from homeassistant.helpers.event import async_call_later, async_track_time_change
from homeassistant.helpers.typing import ConfigType

from .const import (
from homeassistant.helpers.event import async_track_state_change_event, async_track_time_change, async_call_later
    DOMAIN,
    DATA_CTRL,
    STORAGE_KEY,
    STORAGE_VERSION,
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
    SERVICE_HEALTH_CHECK,
    SERVICE_TEST_INDICATOR,
    SERVICE_TEST_SIREN,
    SERVICE_ACK_ALARM,
)

PLATFORMS = ["alarm_control_panel"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ctrl = AlarmController(hass, entry)
    await ctrl.async_setup()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {DATA_CTRL: ctrl}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # services (bound per entry via target entity)
    async def _health_check(call):
        await ctrl.async_health_check()

    async def _test_indicator(call):
        await ctrl.async_test_indicator()

    async def _test_siren(call):
        await ctrl.async_test_siren()

    async def _ack_alarm(call):
        await ctrl.async_ack_alarm()

    hass.services.async_register(DOMAIN, SERVICE_HEALTH_CHECK, _health_check)
    hass.services.async_register(DOMAIN, SERVICE_TEST_INDICATOR, _test_indicator)
    hass.services.async_register(DOMAIN, SERVICE_TEST_SIREN, _test_siren)
    hass.services.async_register(DOMAIN, SERVICE_ACK_ALARM, _ack_alarm)

    entry.async_on_unload(entry.add_update_listener(_update_listener))
    return True


async def _update_listener(hass: HomeAssistant, entry: ConfigEntry):
    ctrl: AlarmController = hass.data[DOMAIN][entry.entry_id][DATA_CTRL]
    await ctrl.async_reload_options()


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    data = hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    if data:
        ctrl: AlarmController = data[DATA_CTRL]
        await ctrl.async_unload()
    return unloaded


class AlarmController:
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self._state = "disarmed"  # disarmed|arming|armed|pending|triggered
        self._exit_task = None
        self._entry_task = None
        self._blink_task = None
        self._siren_task = None
        self._lock = asyncio.Lock()
        self._store = storage.Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._auto_disarm_unsub = None

    # ----- Properties from options
    @property
    def indicator(self) -> str | None:
        return self.entry.options.get(CONF_INDICATOR)

    @property
    def siren_player(self) -> str | None:
        return self.entry.options.get(CONF_SIREN_PLAYER)

    @property
    def siren_volume(self) -> float:
        return float(self.entry.options.get(CONF_SIREN_VOLUME, 1.0))

    @property
    def mp3_source(self) -> str | None:
        return self.entry.options.get(CONF_MP3_SOURCE)

    @property
    def entry_sensors(self) -> List[str]:
        return list(self.entry.options.get(CONF_ENTRY_SENSORS, []))

    @property
    def nfc_tag_id(self) -> str | None:
        return self.entry.options.get(CONF_NFC_TAG_ID)

    @property
    def exit_delay(self) -> int:
        return int(self.entry.options.get(CONF_EXIT_DELAY, 30))

    @property
    def entry_delay(self) -> int:
        return int(self.entry.options.get(CONF_ENTRY_DELAY, 30))

    @property
    def accept_any_when_triggered(self) -> bool:
        return bool(self.entry.options.get(CONF_ACCEPT_ANY_WHEN_TRIGGERED, True))

    @property
    def auto_disarm_time(self) -> str | None:
        return self.entry.options.get(CONF_AUTO_DISARM_TIME)

    # ----- Lifecycle
    async def async_setup(self) -> None:
        await self._async_restore()
        await self.async_reload_options()

        # listen sensors
        if self.entry_sensors:
            self._unsubs = []
            for ent in self.entry_sensors:
                unsub = async_track_state_change_event(
                    ent, self._sensor_changed
                )
                self._unsubs.append(unsub)

        # listen tags
        self._unsub_tag = self.hass.bus.async_listen("tag_scanned", self._tag_scanned)

    async def async_unload(self) -> None:
        if hasattr(self, "_unsubs"):
            for u in self._unsubs:
                u()
        if getattr(self, "_unsub_tag", None):
            self._unsub_tag()
        if self._auto_disarm_unsub:
            self._auto_disarm_unsub()
        await self._async_save()

    async def async_reload_options(self) -> None:
        # reschedule auto-disarm
        if self._auto_disarm_unsub:
            self._auto_disarm_unsub()
            self._auto_disarm_unsub = None

        t = self.auto_disarm_time
        if t:
            try:
                hh, mm, ss = [int(x) for x in t.split(":")]
            except Exception:
                hh, mm, ss = 6, 0, 0
            self._auto_disarm_unsub = async_track_time_change(
                self.hass,
                lambda *_: self.async_disarm(reason="auto_disarm"),
                hour=hh,
                minute=mm,
                second=ss,
            )

    # ----- Persistence
    async def _async_restore(self):
        data = await self._store.async_load()
        if isinstance(data, dict):
            self._state = data.get("state", "disarmed")

    async def _async_save(self):
        await self._store.async_save({"state": self._state})

    # ----- Events
    async def _sensor_changed(self, event):
        new_state = event.data.get("new_state")
        if not new_state or new_state.state != "on":
            return
        if self._state == "armed":
            await self._start_entry_delay()

    async def _tag_scanned(self, event):
        tag_id = event.data.get("tag_id")
        if not tag_id:
            return
        if self._state in ("arming", "armed", "pending", "triggered"):
            if self.accept_any_when_triggered and self._state == "triggered":
                await self.async_disarm(reason="tag_any")
                return
            if tag_id == self.nfc_tag_id:
                await self.async_disarm(reason="tag_match")

    # ----- Public actions
    async def async_arm(self) -> None:
        async with self._lock:
            if self._state in ("arming", "armed"):
                return
            self._state = "arming"
            await self._async_save()
            await self._blink("yellow", times=2)
            self._exit_task = async_call_later(self.hass, self.exit_delay, self._finish_arm)

    async def _finish_arm(self, _now=None):
        async with self._lock:
            if self._state != "arming":
                return
            self._state = "armed"
            await self._async_save()
            await self._blink("blue", times=2)

    async def async_disarm(self, reason: str = "") -> None:
        async with self._lock:
            self._state = "disarmed"
            await self._async_save()
            # cancel timers/blinks/siren
            for t in (self._exit_task, self._entry_task, self._blink_task, self._siren_task):
                if t and hasattr(t, "cancel"):
                    t.cancel()
            await self._light("off")
            # stop current media
            if self.siren_player:
                await self.hass.services.async_call(
                    "media_player",
                    "media_stop",
                    {"entity_id": self.siren_player},
                    blocking=False,
                )

    async def async_trigger(self) -> None:
        async with self._lock:
            self._state = "triggered"
            await self._async_save()
            await self._blink("red", times=0, continuous=True)
            await self._play_mp3()

    async def async_ack_alarm(self) -> None:
        # Stop blinking/siren but keep state as triggered
        if self._blink_task and hasattr(self._blink_task, "cancel"):
            self._blink_task.cancel()
        if self.siren_player:
            await self.hass.services.async_call(
                "media_player",
                "media_stop",
                {"entity_id": self.siren_player},
                blocking=False,
            )

    async def async_health_check(self) -> None:
        # no-op placeholder for now
        return

    async def async_test_indicator(self) -> None:
        await self._blink("green", times=2)

    async def async_test_siren(self) -> None:
        await self._play_mp3()

    # ----- Helpers
    async def _start_entry_delay(self):
        # Already counting?
        if self._entry_task:
            return
        await self._light("on", color="orange", bri=255)
        self._entry_task = async_call_later(self.hass, self.entry_delay, self._entry_timeout)

    async def _entry_timeout(self, _now=None):
        self._entry_task = None
        if self._state == "armed":
            await self.async_trigger()

    async def _light(self, mode: str, color: str | None = None, bri: int | None = None):
        if not self.indicator:
            return
        if mode == "off":
            await self.hass.services.async_call("light", "turn_off", {"entity_id": self.indicator}, blocking=False)
            return
        data = {"entity_id": self.indicator}
        if color:
            data["color_name"] = color
        if bri:
            data["brightness"] = bri
        await self.hass.services.async_call("light", "turn_on", data, blocking=False)

    async def _blink(self, color: str, times: int = 2, continuous: bool = False):
        if not self.indicator:
            return

        async def _runner():
            count = 0
            while continuous or count < times:
                await self._light("on", color=color, bri=255)
                await asyncio.sleep(0.6)
                await self._light("off")
                await asyncio.sleep(0.4)
                count += 1

        # cancel previous
        if self._blink_task and hasattr(self._blink_task, "cancel"):
            self._blink_task.cancel()
        loop = asyncio.create_task(_runner())
        self._blink_task = loop

    async def _play_mp3(self):
        if not self.siren_player or not self.mp3_source:
            return
        # kick cast pipeline
        await self.hass.services.async_call(
            "media_player",
            "play_media",
            {
                "entity_id": self.siren_player,
                "media_content_id": "https://cast.home-assistant.io/redirect",
                "media_content_type": "audio/mp3",
            },
            blocking=False,
        )
        # set volume
        await self.hass.services.async_call(
            "media_player",
            "volume_set",
            {"entity_id": self.siren_player, "volume_level": self.siren_volume},
            blocking=False,
        )
        await asyncio.sleep(0.5)
        await self.hass.services.async_call(
            "media_player",
            "play_media",
            {
                "entity_id": self.siren_player,
                "media_content_id": self.mp3_source,
                "media_content_type": "music",
            },
            blocking=False,
        )