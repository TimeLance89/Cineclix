from __future__ import annotations

import asyncio
import mimetypes
from typing import TYPE_CHECKING, Any, Callable, Optional

import voluptuous as vol
from homeassistant.components.alarm_control_panel import (
    AlarmControlPanelEntity,
    AlarmControlPanelEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers import entity_platform
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import StateType

try:
    from homeassistant.components.alarm_control_panel import AlarmControlPanelState
except ImportError:  # pragma: no cover - backwards compatibility with older HA
    from homeassistant.const import (  # type: ignore[no-redef]
        STATE_ALARM_ARMED_AWAY,
        STATE_ALARM_ARMED_HOME,
        STATE_ALARM_ARMING,
        STATE_ALARM_DISARMED,
        STATE_ALARM_PENDING,
        STATE_ALARM_TRIGGERED,
    )
else:
    STATE_ALARM_ARMED_AWAY = AlarmControlPanelState.ARMED_AWAY
    STATE_ALARM_ARMED_HOME = AlarmControlPanelState.ARMED_HOME
    STATE_ALARM_ARMING = AlarmControlPanelState.ARMING
    STATE_ALARM_DISARMED = AlarmControlPanelState.DISARMED
    STATE_ALARM_PENDING = AlarmControlPanelState.PENDING
    STATE_ALARM_TRIGGERED = AlarmControlPanelState.TRIGGERED

from .const import (
    DOMAIN,
    CONF_INDICATOR_LIGHT,
    CONF_SIREN_PLAYER,
    CONF_SIREN_VOLUME,
    CONF_MP3_FILE,
    CONF_EXIT_DELAY,
    CONF_EXIT_DELAY_SOUND,
    CONF_ENTRY_DELAY_SOUND,
    CONF_CHIME_VOLUME,
    DEFAULT_EXIT_DELAY,
    DEFAULT_CHIME_VOLUME,
    EVENT_ENTRY_DELAY_STARTED,
    EVENT_ENTRY_DELAY_CANCELLED,
    TAG_ACTION_EVENT,
    TAG_ACTION_ARM_AWAY,
    TAG_ACTION_ARM_HOME,
    TAG_ACTION_DISARM,
)

if TYPE_CHECKING:
    from . import AlarmController


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    platform = entity_platform.async_get_current_platform()
    domain_data = hass.data.setdefault(DOMAIN, {})
    if not domain_data.get("_entity_services_registered"):
        platform.async_register_entity_service(
            "play_selected_tone",
            {
                vol.Optional("media_path"): str,
                vol.Optional("volume"): vol.All(
                    vol.Coerce(float), vol.Range(min=0.0, max=1.0)
                ),
            },
            "async_play_selected_tone",
        )
        domain_data["_entity_services_registered"] = True

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
        self._controller: AlarmController = hass.data[DOMAIN][entry.entry_id]
        self._indicator_task: Optional[asyncio.Task] = None
        self._delay_audio_task: Optional[asyncio.Task] = None
        self._arming_cancel: Optional[Callable[[], None]] = None
        self._pre_pending_state: Optional[str] = None
        self._attrs: dict[str, Any] = {
            "entry_delay_active": False,
            "last_tag_action": None,
        }

        # listeners for custom bus events from controller
        self._unsubs.append(
            self.hass.bus.async_listen(f"{DOMAIN}_trigger", self._handle_trigger)
        )
        self._unsubs.append(
            self.hass.bus.async_listen(
                f"{DOMAIN}_disarm_request", self._handle_disarm_request
            )
        )
        self._unsubs.append(
            self.hass.bus.async_listen(f"{DOMAIN}_auto_disarm", self._handle_auto_disarm)
        )
        self._unsubs.append(
            self.hass.bus.async_listen(
                EVENT_ENTRY_DELAY_STARTED, self._handle_entry_delay_started
            )
        )
        self._unsubs.append(
            self.hass.bus.async_listen(
                EVENT_ENTRY_DELAY_CANCELLED, self._handle_entry_delay_cancelled
            )
        )
        self._unsubs.append(
            self.hass.bus.async_listen(TAG_ACTION_EVENT, self._handle_tag_action)
        )

        # Ensure controller knows the initial state
        self._controller.state = self._state

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(identifiers={(DOMAIN, "ha_alarm_pro")}, name="HA Alarm Pro")

    @property
    def state(self) -> StateType:
        return self._state

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self._attrs

    async def async_added_to_hass(self) -> None:
        last = await self.async_get_last_state()
        if last:
            self._state = last.state or STATE_ALARM_DISARMED
            self._controller.state = self._state
            if last.attributes:
                self._attrs.update(last.attributes)
                self._attrs["entry_delay_active"] = False
                self._attrs.pop("entry_delay_seconds", None)

        self.async_on_remove(self.entry.add_update_listener(self._handle_entry_update))

    async def _handle_entry_update(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self._cfg = entry.options or entry.data

    def _set_state(self, new_state: str) -> None:
        self._state = new_state
        self._controller.state = new_state
        self.async_write_ha_state()

    def _cancel_arming_timer(self) -> None:
        if self._arming_cancel:
            cancel = self._arming_cancel
            self._arming_cancel = None
            try:
                cancel()
            except Exception:
                pass

    def _indicator_lights(self) -> list[str]:
        lights = self._cfg.get(CONF_INDICATOR_LIGHT)
        if not lights:
            return []
        if isinstance(lights, str):
            return [lights]
        if isinstance(lights, (list, tuple, set)):
            return [str(item) for item in lights if item]
        return [str(lights)]

    async def _flash_indicator(
        self, flashes: int = 2, color: str | None = None, interval: float = 0.3
    ) -> None:
        lights = self._indicator_lights()
        if not lights:
            return
        self._stop_indicator_loop()
        data_on: dict[str, Any] = {"entity_id": lights, "brightness_pct": 100}
        if color:
            data_on["color_name"] = color
        for _ in range(flashes):
            await self.hass.services.async_call(
                "light", "turn_on", data_on, blocking=True
            )
            await asyncio.sleep(interval)
            await self.hass.services.async_call(
                "light", "turn_off", {"entity_id": lights}, blocking=True
            )
            await asyncio.sleep(interval)

    def _start_indicator_loop(
        self, color: str | None = None, on_time: float = 0.6, off_time: float = 0.4
    ) -> None:
        lights = self._indicator_lights()
        if not lights:
            return
        self._stop_indicator_loop()

        async def _loop() -> None:
            try:
                data_on: dict[str, Any] = {"entity_id": lights, "brightness_pct": 100}
                if color:
                    data_on["color_name"] = color
                while True:
                    await self.hass.services.async_call(
                        "light", "turn_on", data_on, blocking=True
                    )
                    await asyncio.sleep(on_time)
                    await self.hass.services.async_call(
                        "light", "turn_off", {"entity_id": lights}, blocking=True
                    )
                    await asyncio.sleep(off_time)
            except asyncio.CancelledError:  # pragma: no cover - best effort clean up
                pass
            finally:
                await self.hass.services.async_call(
                    "light", "turn_off", {"entity_id": lights}, blocking=False
                )

        self._indicator_task = self.hass.loop.create_task(_loop())

    def _stop_indicator_loop(self) -> None:
        if self._indicator_task:
            self._indicator_task.cancel()
            self._indicator_task = None
        lights = self._indicator_lights()
        if lights:
            self.hass.async_create_task(
                self.hass.services.async_call(
                    "light", "turn_off", {"entity_id": lights}, blocking=False
                )
            )

    def _resolve_media(self, mp3: str) -> tuple[str, str]:
        """Return (media_content_id, media_content_type)."""
        if not mp3:
            return "", ""
        if mp3.startswith("media-source://"):
            return mp3, "music"
        media_type, _ = mimetypes.guess_type(mp3)
        if media_type and media_type.startswith("audio/"):
            return mp3, media_type
        if media_type:
            return mp3, media_type
        return mp3, "music"

    def _stop_delay_audio(self) -> None:
        if self._delay_audio_task:
            self._delay_audio_task.cancel()
            self._delay_audio_task = None

    def _start_delay_audio(self, sound: str | None, duration: int, kind: str) -> None:
        self._stop_delay_audio()
        if not sound:
            return
        if duration <= 0:
            return
        player = self._cfg.get(CONF_SIREN_PLAYER)
        if not player:
            return

        chime_volume = self._cfg.get(CONF_CHIME_VOLUME, DEFAULT_CHIME_VOLUME)

        async def _loop() -> None:
            remaining = max(int(duration), 0)
            first = True
            try:
                while remaining > 0:
                    await self._play_media(sound, volume=chime_volume if first else None)
                    first = False
                    if remaining <= 5:
                        wait = 1
                    elif remaining <= 15:
                        wait = 1 if kind == "entry" else 2
                    elif remaining <= 30:
                        wait = 2 if kind == "entry" else 3
                    else:
                        wait = 5
                    wait = max(1, min(wait, remaining))
                    await asyncio.sleep(wait)
                    remaining -= wait
            except asyncio.CancelledError:  # pragma: no cover - best effort clean up
                pass

        self._delay_audio_task = self.hass.loop.create_task(_loop())

    async def _play_media(self, media: str, *, volume: float | None = None) -> None:
        player = self._cfg.get(CONF_SIREN_PLAYER)
        if not player or not media:
            return
        if volume is not None:
            try:
                level = max(0.0, min(float(volume), 1.0))
            except (TypeError, ValueError):
                level = DEFAULT_CHIME_VOLUME
            await self.hass.services.async_call(
                "media_player",
                "volume_set",
                {"entity_id": player, "volume_level": level},
                blocking=True,
            )
        media_content_id, media_type = self._resolve_media(media)
        await self.hass.services.async_call(
            "media_player",
            "play_media",
            {
                "entity_id": player,
                "media_content_id": media_content_id,
                "media_content_type": media_type if media_type else "music",
            },
            blocking=False,
        )

    async def _play_siren(self) -> None:
        player = self._cfg.get(CONF_SIREN_PLAYER)
        mp3 = self._cfg.get(CONF_MP3_FILE)
        volume = self._cfg.get(CONF_SIREN_VOLUME, 1)
        if not player or not mp3:
            return
        await self._play_media(mp3, volume=volume)

    async def _stop_siren(self) -> None:
        player = self._cfg.get(CONF_SIREN_PLAYER)
        if not player:
            return
        await self.hass.services.async_call(
            "media_player", "media_stop", {"entity_id": player}, blocking=False
        )

    async def async_play_selected_tone(
        self, media_path: str | None = None, volume: float | None = None
    ) -> None:
        media = media_path if media_path is not None else self._cfg.get(CONF_MP3_FILE)
        if not media:
            return
        if volume is None:
            volume = self._cfg.get(CONF_SIREN_VOLUME, 1)
        await self._play_media(media, volume=volume)

    async def _begin_arming(self, target_state: str) -> None:
        self._controller.cancel_pending()
        self._stop_indicator_loop()
        self._stop_delay_audio()
        self._cancel_arming_timer()
        self._pre_pending_state = None
        self._attrs["entry_delay_active"] = False
        self._attrs.pop("entry_delay_seconds", None)
        self._set_state(STATE_ALARM_ARMING)
        await self._flash_indicator(2, color="yellow")
        delay = int(self._cfg.get(CONF_EXIT_DELAY, DEFAULT_EXIT_DELAY))
        if delay <= 0:
            self._stop_delay_audio()
            self._set_state(target_state)
            return

        self._start_delay_audio(self._cfg.get(CONF_EXIT_DELAY_SOUND), delay, "exit")

        def _finish(now) -> None:
            self._arming_cancel = None
            if self._state == STATE_ALARM_ARMING:
                self._stop_delay_audio()
                self._set_state(target_state)

        self._arming_cancel = async_call_later(self.hass, delay, _finish)

    async def async_alarm_arm_home(self, code: str | None = None) -> None:
        await self._begin_arming(STATE_ALARM_ARMED_HOME)

    async def async_alarm_arm_away(self, code: str | None = None) -> None:
        await self._begin_arming(STATE_ALARM_ARMED_AWAY)

    async def async_alarm_disarm(self, code: str | None = None) -> None:
        self._controller.cancel_pending()
        self._stop_indicator_loop()
        self._cancel_arming_timer()
        self._stop_delay_audio()
        await self._stop_siren()
        self._attrs["entry_delay_active"] = False
        self._attrs.pop("entry_delay_seconds", None)
        self._pre_pending_state = None
        self._set_state(STATE_ALARM_DISARMED)

    async def async_alarm_trigger(self, code: str | None = None) -> None:
        if self._state == STATE_ALARM_TRIGGERED:
            return
        self._stop_indicator_loop()
        self._stop_delay_audio()
        self._attrs["entry_delay_active"] = False
        self._attrs.pop("entry_delay_seconds", None)
        self._pre_pending_state = None
        self._set_state(STATE_ALARM_TRIGGERED)
        self._start_indicator_loop(color="red", on_time=1, off_time=1)
        await self._play_siren()

    @callback
    async def _handle_trigger(self, event) -> None:
        if self._state in (
            STATE_ALARM_ARMED_HOME,
            STATE_ALARM_ARMED_AWAY,
            STATE_ALARM_PENDING,
        ):
            source = event.data.get("source")
            if source:
                self._attrs["last_trigger_source"] = source
            await self.async_alarm_trigger()

    @callback
    async def _handle_disarm_request(self, event) -> None:
        tag = event.data.get("tag_id")
        if tag:
            self._attrs["last_disarm_tag"] = tag
        self._attrs["last_tag_action"] = TAG_ACTION_DISARM
        await self.async_alarm_disarm()

    @callback
    async def _handle_auto_disarm(self, event) -> None:
        self._attrs["last_disarm_tag"] = "auto"
        self._attrs["last_tag_action"] = "auto_disarm"
        await self.async_alarm_disarm()

    @callback
    async def _handle_tag_action(self, event) -> None:
        action = event.data.get("action")
        tag = event.data.get("tag_id")
        if tag:
            self._attrs["last_disarm_tag"] = tag
        if action == TAG_ACTION_DISARM:
            self._attrs["last_tag_action"] = TAG_ACTION_DISARM
            await self.async_alarm_disarm()
        elif action == TAG_ACTION_ARM_HOME:
            self._attrs["last_tag_action"] = TAG_ACTION_ARM_HOME
            await self.async_alarm_arm_home()
        elif action == TAG_ACTION_ARM_AWAY:
            self._attrs["last_tag_action"] = TAG_ACTION_ARM_AWAY
            await self.async_alarm_arm_away()

    @callback
    def _handle_entry_delay_started(self, event) -> None:
        if self._state not in (
            STATE_ALARM_ARMED_HOME,
            STATE_ALARM_ARMED_AWAY,
        ):
            return
        self._pre_pending_state = self._state
        delay = event.data.get("delay")
        source = event.data.get("source")
        self._attrs["entry_delay_active"] = True
        if delay is not None:
            self._attrs["entry_delay_seconds"] = delay
            try:
                self._start_delay_audio(
                    self._cfg.get(CONF_ENTRY_DELAY_SOUND), int(delay), "entry"
                )
            except (TypeError, ValueError):
                pass
        if source:
            self._attrs["last_entry_sensor"] = source
        self._set_state(STATE_ALARM_PENDING)
        self._start_indicator_loop(color="orange", on_time=0.6, off_time=0.4)

    @callback
    def _handle_entry_delay_cancelled(self, event) -> None:
        self._attrs["entry_delay_active"] = False
        self._attrs.pop("entry_delay_seconds", None)
        self._stop_indicator_loop()
        self._stop_delay_audio()
        if self._state == STATE_ALARM_PENDING and self._pre_pending_state:
            self._set_state(self._pre_pending_state)
        else:
            self.async_write_ha_state()
        self._pre_pending_state = None

    async def async_will_remove_from_hass(self) -> None:
        self._stop_indicator_loop()
        self._stop_delay_audio()
        self._cancel_arming_timer()
        for unsubscribe in self._unsubs:
            try:
                unsubscribe()
            except Exception:
                pass
        self._unsubs = []
