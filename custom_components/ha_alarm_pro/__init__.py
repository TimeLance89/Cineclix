
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time, timedelta
from typing import Any, Callable, Dict, List, Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, Event, callback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.event import (
    async_track_state_change_event,
    async_track_time_change,
    async_call_later,
)
from homeassistant.helpers.typing import ConfigType
from homeassistant.const import STATE_ON, STATE_OFF

from .const import (
    DOMAIN,
    PLATFORMS,
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

CALLBACK = Callable[[], None]


@dataclass
class AlarmController:
    hass: HomeAssistant
    entry_id: str
    indicator: Optional[str]
    media_player: Optional[str]
    volume: float
    mp3_file: Optional[str]
    sensors: List[str]
    exit_delay: int
    entry_delay: int
    allow_any_tag: bool
    nfc_tag: Optional[str]
    auto_disarm_time: Optional[time]

    # runtime
    armed: bool = False
    triggered: bool = False
    pending: bool = False
    _unsubs: List[CALLBACK] = field(default_factory=list)

    def _media_source_uri(self, path: str) -> Optional[str]:
        if not path:
            return None
        p = path.strip().lstrip("/")
        if p.startswith("media/"):
            return f"media-source://media_source/{p}"
        if p.startswith("local/"):
            # already local prefix
            return f"media-source://media_source/{p}"
        if p.startswith("www/"):
            return f"media-source://media_source/local/{p.split('www/',1)[1]}"
        if p.startswith("config/www/"):
            return f"media-source://media_source/local/{p.split('config/www/',1)[1]}"
        # treat as already relative -> local
        return f"media-source://media_source/local/{p}"

    async def async_setup(self) -> None:
        # track sensors
        if self.sensors:
            unsub = async_track_state_change_event(
                self.hass, self.sensors, self._sensor_changed
            )
            self._unsubs.append(unsub)

        # listen for NFC tag events
        @callback
        def _on_tag(event: Event) -> None:
            if not self.armed:
                return
            tag_id = event.data.get("tag_id")
            if self.allow_any_tag or (self.nfc_tag and tag_id == self.nfc_tag):
                self.hass.create_task(self.async_disarm(source="nfc"))

        self._unsubs.append(self.hass.bus.async_listen("tag_scanned", _on_tag))

        # schedule auto-disarm time
        if self.auto_disarm_time:
            hh, mm, ss = (
                self.auto_disarm_time.hour,
                self.auto_disarm_time.minute,
                self.auto_disarm_time.second,
            )

            def _time_match(now):
                return now.hour == hh and now.minute == mm and now.second == ss

            self._unsubs.append(
                async_track_time_change(
                    self.hass, lambda *_: self.hass.create_task(self.async_disarm(source="schedule")), hour=hh, minute=mm, second=ss
                )
            )

    async def async_unload(self) -> None:
        while self._unsubs:
            unsub = self._unsubs.pop()
            try:
                unsub()
            except Exception:  # noqa: BLE001
                pass

    @callback
    def _sensor_changed(self, event: Event) -> None:
        if not self.armed or self.triggered or self.pending:
            return
        to_state = event.data.get("new_state")
        if not to_state:
            return
        val = to_state.state
        is_on = val not in (STATE_OFF, "off", "idle", "closed", "standby", None, "")
        if is_on:
            # start entry delay then trigger
            self.pending = True
            async_call_later(
                self.hass, self.entry_delay, lambda *_: self.hass.create_task(self._maybe_trigger())
            )

    async def _maybe_trigger(self) -> None:
        self.pending = False
        if not self.armed:
            return
        await self.async_trigger()

    async def async_arm(self) -> None:
        if self.armed or self.pending:
            return
        self.pending = True
        # flash indicator quickly
        await self._flash_indicator(repeat=2)
        async_call_later(self.hass, self.exit_delay, lambda *_: self.hass.create_task(self._finish_arm()))

    async def _finish_arm(self) -> None:
        self.pending = False
        self.armed = True
        await self._flash_indicator(repeat=1)

    async def async_disarm(self, source: str | None = None) -> None:
        self.armed = False
        self.triggered = False
        self.pending = False
        await self._stop_siren()
        await self._indicator_off()

    async def async_trigger(self) -> None:
        if self.triggered:
            return
        self.triggered = True
        await self._play_siren()
        await self._flash_indicator(repeat=6)

    async def _flash_indicator(self, repeat: int = 1) -> None:
        if not self.indicator:
            return
        # best-effort blink without requiring color support
        for _ in range(repeat):
            await self.hass.services.async_call("light", "turn_on", {"entity_id": self.indicator, "brightness_pct": 100}, blocking=False)
            async_call_later(self.hass, 0.3, lambda *_: self.hass.async_create_task(
                self.hass.services.async_call("light", "turn_off", {"entity_id": self.indicator}, blocking=False)
            ))

    async def _indicator_off(self) -> None:
        if self.indicator:
            await self.hass.services.async_call("light", "turn_off", {"entity_id": self.indicator}, blocking=False)

    async def _play_siren(self) -> None:
        if not self.media_player or not self.mp3_file:
            return
        # set volume
        await self.hass.services.async_call(
            "media_player", "volume_set", {"entity_id": self.media_player, "volume_level": self.volume}, blocking=False
        )
        uri = self._media_source_uri(self.mp3_file)
        if not uri:
            return
        await self.hass.services.async_call(
            "media_player",
            "play_media",
            {
                "entity_id": self.media_player,
                "media_content_id": uri,
                "media_content_type": "music",
            },
            blocking=False,
        )

    async def _stop_siren(self) -> None:
        if not self.media_player:
            return
        await self.hass.services.async_call(
            "media_player", "media_stop", {"entity_id": self.media_player}, blocking=False
        )


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data = entry.data
    ctrl = AlarmController(
        hass=hass,
        entry_id=entry.entry_id,
        indicator=data.get(CONF_INDICATOR),
        media_player=data.get(CONF_MEDIA_PLAYER),
        volume=float(data.get(CONF_VOLUME, 1.0)),
        mp3_file=data.get(CONF_MP3),
        sensors=list(data.get(CONF_SENSORS, [])),
        exit_delay=int(data.get(CONF_EXIT_DELAY, 30)),
        entry_delay=int(data.get(CONF_ENTRY_DELAY, 30)),
        allow_any_tag=bool(data.get(CONF_ALLOW_ANY_TAG, False)),
        nfc_tag=data.get(CONF_NFC_TAG),
        auto_disarm_time=data.get(CONF_AUTO_DISARM),
    )
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][entry.entry_id] = ctrl
    await ctrl.async_setup()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ctrl: AlarmController = hass.data[DOMAIN].pop(entry.entry_id)
    await ctrl.async_unload()
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
