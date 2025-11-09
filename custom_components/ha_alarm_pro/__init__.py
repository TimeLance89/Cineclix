
from __future__ import annotations

from typing import Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import (
    async_track_state_change_event,
    async_track_time_change,
    async_call_later,
)
from homeassistant.const import STATE_ON

from .const import (
    DOMAIN,
    CONF_ENTRY_SENSORS,
    CONF_NFC_TAG,
    CONF_ALLOW_ANY_TAG,
    CONF_ENTRY_DELAY,
    CONF_AUTO_DISARM_TIME,
)

PLATFORMS = ["alarm_control_panel"]


class AlarmController:
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self._unsubs: list[Callable[[], None]] = []
        self.state: str = "disarmed"
        self.listeners_ready = False

    async def async_setup(self) -> None:
        await self._attach_listeners()
        self.listeners_ready = True

    async def async_unload(self) -> None:
        for u in self._unsubs:
            try:
                u()
            except Exception:
                pass
        self._unsubs.clear()

    async def _attach_listeners(self) -> None:
        cfg = self.entry.options or self.entry.data
        sensors: list[str] = cfg.get(CONF_ENTRY_SENSORS, [])

        @callback
        def _on_sensor_event(event) -> None:
            # A sensor turned on -> start entry delay or trigger if already armed_away
            to_state = event.data.get("new_state")
            if not to_state:
                return
            if to_state.state != STATE_ON:
                return
            if self.state in ("armed_away", "armed_home"):
                entry_delay = int(cfg.get(CONF_ENTRY_DELAY, 30))
                # Schedule trigger
                async def delayed_trigger(now):
                    if self.state in ("armed_away", "armed_home"):
                        self.hass.bus.async_fire(f"{DOMAIN}_trigger", {"source": to_state.entity_id})
                self._unsubs.append(async_call_later(self.hass, entry_delay, delayed_trigger))

        if sensors:
            self._unsubs.append(async_track_state_change_event(self.hass, sensors, _on_sensor_event))

        # Tag scanned -> disarm if matches
        @callback
        def _on_tag_scanned(event):
            tag_id = event.data.get("tag_id")
            allow_any = bool(cfg.get(CONF_ALLOW_ANY_TAG, False))
            wanted = cfg.get(CONF_NFC_TAG)
            if allow_any or (wanted and wanted == tag_id):
                self.hass.bus.async_fire(f"{DOMAIN}_disarm_request", {"tag_id": tag_id})

        self._unsubs.append(self.hass.bus.async_listen("tag_scanned", _on_tag_scanned))

        # Auto disarm at a time
        auto = cfg.get(CONF_AUTO_DISARM_TIME)
        if auto:
            try:
                hh, mm, ss = [int(x) for x in auto.split(":")]
                def _cb(hass_time):
                    self.hass.bus.async_fire(f"{DOMAIN}_auto_disarm", {})
                self._unsubs.append(async_track_time_change(self.hass, _cb, hour=hh, minute=mm, second=ss))
            except Exception:
                pass


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
