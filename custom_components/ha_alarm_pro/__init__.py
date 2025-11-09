from __future__ import annotations

from typing import Callable, Optional, Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import (
    async_track_state_change_event,
    async_track_time_change,
    async_call_later,
)
from homeassistant.const import STATE_ON

# Preload platforms to avoid blocking imports during setup
from . import alarm_control_panel  # noqa: F401

from .const import (
    DOMAIN,
    CONF_ENTRY_SENSORS,
    CONF_INDICATOR_LIGHT,
    CONF_NFC_TAG,
    CONF_ALLOW_ANY_TAG,
    CONF_ACCEPT_ANY_TAG_WHEN_TRIGGERED,
    CONF_ENTRY_DELAY,
    CONF_AUTO_DISARM_TIME,
    CONF_AUTHORIZED_TAGS,
    CONF_TAG_ARMING_MODE,
    DEFAULT_ENTRY_DELAY,
    DEFAULT_TAG_ARMING_MODE,
    EVENT_ENTRY_DELAY_STARTED,
    EVENT_ENTRY_DELAY_CANCELLED,
    TAG_ACTION_EVENT,
    TAG_ACTION_ARM_AWAY,
    TAG_ACTION_ARM_HOME,
    TAG_ACTION_DISARM,
)

PLATFORMS = ["alarm_control_panel"]


def _normalize_tag(value: Optional[str]) -> str:
    if not value:
        return ""
    return str(value).lower().replace("-", "")


def _normalize_state(value: Any) -> str:
    if value is None:
        return "unknown"
    if hasattr(value, "value"):
        return str(value.value)
    return str(value)


def _ensure_list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, (tuple, set)):
        return [*value]
    return [value]


class AlarmController:
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self._unsubs: list[Callable[[], None]] = []
        self._pending_cancel: Optional[Callable[[], None]] = None
        self._pending_source: Optional[str] = None
        self._state: str = "disarmed"
        self.listeners_ready = False

    async def async_setup(self) -> None:
        await self._attach_listeners()
        self.listeners_ready = True

    async def async_unload(self) -> None:
        self.cancel_pending()
        for unsub in self._unsubs:
            try:
                unsub()
            except Exception:
                pass
        self._unsubs.clear()

    async def _attach_listeners(self) -> None:
        cfg = self.entry.options or self.entry.data
        sensors_raw = cfg.get(CONF_ENTRY_SENSORS) or []
        sensors: list[str] = list(sensors_raw if isinstance(sensors_raw, list) else [sensors_raw])

        @callback
        def _on_sensor_event(event) -> None:
            to_state = event.data.get("new_state")
            if not to_state:
                return
            if to_state.state != STATE_ON:
                return
            if self.state in ("armed_away", "armed_home"):
                self._start_entry_delay(cfg, to_state.entity_id)

        if sensors:
            self._unsubs.append(
                async_track_state_change_event(self.hass, sensors, _on_sensor_event)
            )

        @callback
        def _on_tag_scanned(event):
            tag_id = event.data.get("tag_id")
            if not tag_id:
                return
            allow_any = bool(cfg.get(CONF_ALLOW_ANY_TAG, False))
            allow_any_when_triggered = bool(
                cfg.get(CONF_ACCEPT_ANY_TAG_WHEN_TRIGGERED, False)
            )
            normalized_tag = _normalize_tag(tag_id)
            if not normalized_tag:
                return

            configured_tags = {
                _normalize_tag(tag)
                for tag in _ensure_list(cfg.get(CONF_AUTHORIZED_TAGS) or cfg.get(CONF_NFC_TAG))
                if _normalize_tag(tag)
            }

            current_state = self.state
            is_authorized = allow_any or normalized_tag in configured_tags
            action: str | None = None

            if current_state == "disarmed":
                if is_authorized:
                    mode = str(cfg.get(CONF_TAG_ARMING_MODE, DEFAULT_TAG_ARMING_MODE))
                    action = (
                        TAG_ACTION_ARM_HOME
                        if mode == TAG_ACTION_ARM_HOME
                        else TAG_ACTION_ARM_AWAY
                    )
            elif current_state in ("arming", "armed_home", "armed_away", "pending"):
                if is_authorized:
                    action = TAG_ACTION_DISARM
            elif current_state == "triggered":
                if allow_any_when_triggered or is_authorized:
                    action = TAG_ACTION_DISARM

            if action:
                if action == TAG_ACTION_DISARM:
                    self.cancel_pending()
                self.hass.bus.async_fire(
                    TAG_ACTION_EVENT,
                    {"tag_id": tag_id, "action": action},
                )

        self._unsubs.append(self.hass.bus.async_listen("tag_scanned", _on_tag_scanned))

        auto = cfg.get(CONF_AUTO_DISARM_TIME)
        if auto:
            try:
                hh, mm, ss = [int(x) for x in auto.split(":")]

                def _cb(hass_time):
                    self.hass.bus.async_fire(f"{DOMAIN}_auto_disarm", {})

                self._unsubs.append(
                    async_track_time_change(
                        self.hass, _cb, hour=hh, minute=mm, second=ss
                    )
                )
            except Exception:
                pass

    def _start_entry_delay(self, cfg: dict, sensor_entity: str) -> None:
        entry_delay = int(cfg.get(CONF_ENTRY_DELAY, DEFAULT_ENTRY_DELAY))
        if entry_delay <= 0:
            self.hass.bus.async_fire(f"{DOMAIN}_trigger", {"source": sensor_entity})
            return

        self.cancel_pending(notify=False)
        self._pending_source = sensor_entity
        self.hass.bus.async_fire(
            EVENT_ENTRY_DELAY_STARTED,
            {"source": sensor_entity, "delay": entry_delay},
        )

        def _finish(now) -> None:
            self._pending_cancel = None
            source = sensor_entity
            if self.state in ("armed_away", "armed_home"):
                self.hass.bus.async_fire(f"{DOMAIN}_trigger", {"source": source})

        self._pending_cancel = async_call_later(self.hass, entry_delay, _finish)

    def cancel_pending(self, notify: bool = True) -> None:
        if self._pending_cancel:
            cancel = self._pending_cancel
            self._pending_cancel = None
            try:
                cancel()
            except Exception:
                pass
            if notify:
                self.hass.bus.async_fire(
                    EVENT_ENTRY_DELAY_CANCELLED,
                    {"source": self._pending_source},
                )
        elif notify and self._pending_source:
            self.hass.bus.async_fire(
                EVENT_ENTRY_DELAY_CANCELLED,
                {"source": self._pending_source},
            )
        self._pending_source = None


    @property
    def state(self) -> str:
        return self._state

    @state.setter
    def state(self, value: Any) -> None:
        self._state = _normalize_state(value)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    controller = AlarmController(hass, entry)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = controller
    await controller.async_setup()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    controller: AlarmController = hass.data[DOMAIN].pop(entry.entry_id)
    await controller.async_unload()
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return unload_ok


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update if needed."""
    ctrl: AlarmController = hass.data[DOMAIN][entry.entry_id]
    await ctrl.async_unload()
    await ctrl.async_setup()


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    version = entry.version
    data = dict(entry.data)
    options = dict(entry.options)
    migrated = False

    def _migrate(container: dict) -> bool:
        updated = False
        if container is None:
            return False
        if container.get(CONF_INDICATOR_LIGHT) is not None:
            indicator_list = _ensure_list(container.get(CONF_INDICATOR_LIGHT))
            if container.get(CONF_INDICATOR_LIGHT) != indicator_list:
                container[CONF_INDICATOR_LIGHT] = indicator_list
                updated = True
        if CONF_AUTHORIZED_TAGS not in container:
            legacy_tag = container.pop(CONF_NFC_TAG, None)
            tags_list = _ensure_list(legacy_tag)
            container[CONF_AUTHORIZED_TAGS] = tags_list
            updated = True
        else:
            container[CONF_AUTHORIZED_TAGS] = _ensure_list(
                container.get(CONF_AUTHORIZED_TAGS)
            )
        if CONF_TAG_ARMING_MODE not in container:
            container[CONF_TAG_ARMING_MODE] = DEFAULT_TAG_ARMING_MODE
            updated = True
        return updated

    if version < 2:
        if _migrate(data):
            migrated = True
        if _migrate(options):
            migrated = True
        entry.version = 2
        migrated = True

    if migrated:
        hass.config_entries.async_update_entry(entry, data=data, options=options)

    return True
