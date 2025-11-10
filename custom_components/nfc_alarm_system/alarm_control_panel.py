"""Alarm Control Panel for NFC Alarm System."""
import logging
import asyncio
from datetime import timedelta
from typing import Any

from homeassistant.components.alarm_control_panel import (
    AlarmControlPanelEntity,
    AlarmControlPanelEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import (
    async_track_time_interval,
    async_track_point_in_time,
    async_track_state_change_event,
)
from homeassistant.util import dt as dt_util
from homeassistant.const import CONF_NAME
from homeassistant.components.alarm_control_panel.const import (
    AlarmControlPanelState,
)

from .const import (
    DOMAIN,
    CONF_INDICATOR_LIGHTS,
    CONF_TRIGGER_SENSORS,
    CONF_NFC_TAGS,
    CONF_USE_SINGLE_TAG,
    CONF_ARM_TAG,
    CONF_DISARM_TAG,
    CONF_MEDIA_PLAYER,
    CONF_SIREN_FILE,
    CONF_ENABLE_SIREN,
    CONF_EXIT_DELAY,
    CONF_ENTRY_DELAY,
    CONF_AUTO_DISARM_TIME,
    CONF_ENABLE_AUTO_DISARM,
    CONF_NOTIFY_SERVICE,
    CONF_ENABLE_NOTIFICATIONS,
    COLOR_GREEN,
    COLOR_YELLOW,
    COLOR_ORANGE,
    COLOR_BLUE,
    COLOR_RED,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the NFC Alarm System alarm control panel."""
    config = config_entry.data
    
    alarm_panel = NFCAlarmPanel(hass, config, config_entry.entry_id)
    async_add_entities([alarm_panel])


class NFCAlarmPanel(AlarmControlPanelEntity):
    """Representation of an NFC Alarm System."""

    def __init__(self, hass: HomeAssistant, config: dict, entry_id: str) -> None:
        """Initialize the alarm panel."""
        self.hass = hass
        self._config = config
        self._entry_id = entry_id
        self._attr_name = config.get(CONF_NAME, "NFC Alarmsystem")
        self._attr_unique_id = f"{DOMAIN}_{entry_id}"
        
        # State variables
        self._state = AlarmControlPanelState.DISARMED
        self._arming_task = None
        self._entry_delay_task = None
        self._trigger_task = None
        self._auto_disarm_cancel = None
        
        # Configuration
        self._indicator_lights = config.get(CONF_INDICATOR_LIGHTS, [])
        self._trigger_sensors = config.get(CONF_TRIGGER_SENSORS, [])
        self._use_single_tag = config.get(CONF_USE_SINGLE_TAG, True)
        self._arm_tag = config.get(CONF_ARM_TAG, "").lower().replace("-", "")
        self._disarm_tag = config.get(CONF_DISARM_TAG, "").lower().replace("-", "")
        self._media_player = config.get(CONF_MEDIA_PLAYER)
        self._siren_file = config.get(CONF_SIREN_FILE, "")
        self._enable_siren = config.get(CONF_ENABLE_SIREN, False)
        self._exit_delay = config.get(CONF_EXIT_DELAY, 120)
        self._entry_delay = config.get(CONF_ENTRY_DELAY, 30)
        self._auto_disarm_time = config.get(CONF_AUTO_DISARM_TIME)
        self._enable_auto_disarm = config.get(CONF_ENABLE_AUTO_DISARM, False)
        self._notify_service = config.get(CONF_NOTIFY_SERVICE, "")
        self._enable_notifications = config.get(CONF_ENABLE_NOTIFICATIONS, False)
        
        # Supported features
        self._attr_supported_features = (
            AlarmControlPanelEntityFeature.ARM_AWAY
        )

    async def async_added_to_hass(self) -> None:
        """Run when entity is added to hass."""
        # Listen for tag scanned events
        self.hass.bus.async_listen("tag_scanned", self._handle_tag_scanned)
        
        # Listen for trigger sensor state changes
        for sensor in self._trigger_sensors:
            async_track_state_change_event(
                self.hass, sensor, self._handle_sensor_triggered
            )
        
        # Setup auto disarm if enabled
        if self._enable_auto_disarm and self._auto_disarm_time:
            await self._setup_auto_disarm()

    async def _setup_auto_disarm(self):
        """Setup automatic disarm at specified time."""
        async def auto_disarm_callback(now):
            """Disarm the alarm automatically."""
            if self._state in [AlarmControlPanelState.ARMED_AWAY, AlarmControlPanelState.TRIGGERED]:
                await self.async_alarm_disarm()
                await self._send_notification(
                    "Alarm unscharf",
                    f"Automatisch um {self._auto_disarm_time} deaktiviert."
                )
        
        # Schedule daily at specified time
        time_parts = self._auto_disarm_time.split(":")
        if len(time_parts) == 3:
            hour, minute, second = map(int, time_parts)
            
            async def schedule_next():
                now = dt_util.now()
                target = now.replace(hour=hour, minute=minute, second=second, microsecond=0)
                if target <= now:
                    target += timedelta(days=1)
                
                self._auto_disarm_cancel = async_track_point_in_time(
                    self.hass, auto_disarm_callback, target
                )
            
            await schedule_next()

    @callback
    async def _handle_tag_scanned(self, event):
        """Handle NFC tag scanned event."""
        tag_id = event.data.get("tag_id", "").lower().replace("-", "")
        
        if not tag_id:
            return
        
        # Check if tag is authorized
        is_arm_tag = (tag_id == self._arm_tag)
        is_disarm_tag = (tag_id == self._disarm_tag) if not self._use_single_tag else is_arm_tag
        
        if not (is_arm_tag or is_disarm_tag):
            return
        
        _LOGGER.debug(f"Authorized tag scanned: {tag_id}, current state: {self._state}")
        
        # Handle based on current state
        if self._state in [AlarmControlPanelState.ARMED_AWAY, AlarmControlPanelState.TRIGGERED]:
            # Disarm
            if is_disarm_tag or self._use_single_tag:
                await self._disarm_sequence()
        
        elif self._state == AlarmControlPanelState.ARMING:
            # Cancel arming
            await self._cancel_arming()
        
        elif self._state == AlarmControlPanelState.PENDING:
            # Disarm during entry delay
            if is_disarm_tag or self._use_single_tag:
                await self._disarm_sequence()
        
        elif self._state == AlarmControlPanelState.DISARMED:
            # Start arming sequence
            if is_arm_tag or self._use_single_tag:
                await self._start_arming_sequence()

    async def _start_arming_sequence(self):
        """Start the arming sequence with exit delay."""
        self._state = AlarmControlPanelState.ARMING
        self.async_write_ha_state()
        
        # Visual feedback - yellow blink
        await self._blink_lights(COLOR_YELLOW, 2)
        
        # Send notification
        await self._send_notification(
            "Armierung gestartet",
            f"Scharf in {self._exit_delay} s. Erneutes NFC = Abbruch."
        )
        
        # Wait for exit delay or tag scan
        try:
            await asyncio.sleep(self._exit_delay)
            
            # If we get here, no cancellation occurred
            await self._arm_alarm()
            
        except asyncio.CancelledError:
            _LOGGER.debug("Arming sequence cancelled")

    async def _cancel_arming(self):
        """Cancel the arming sequence."""
        if self._arming_task:
            self._arming_task.cancel()
            self._arming_task = None
        
        self._state = AlarmControlPanelState.DISARMED
        self.async_write_ha_state()
        
        # Visual feedback - orange
        await self._set_light_color(COLOR_ORANGE, duration=0.6)
        
        await self._send_notification(
            "Armierung abgebrochen",
            "NFC erneut gescannt – bleibt unscharf."
        )

    async def _arm_alarm(self):
        """Arm the alarm."""
        self._state = AlarmControlPanelState.ARMED_AWAY
        self.async_write_ha_state()
        
        # Visual feedback - blue blink
        await self._blink_lights(COLOR_BLUE, 2)
        
        await self._send_notification(
            "Alarm scharf",
            "Armierung aktiv."
        )

    async def _disarm_sequence(self):
        """Disarm the alarm."""
        # Stop any running tasks
        if self._arming_task:
            self._arming_task.cancel()
        if self._entry_delay_task:
            self._entry_delay_task.cancel()
        if self._trigger_task:
            self._trigger_task.cancel()
        
        # Stop siren if playing
        if self._enable_siren and self._media_player:
            await self.hass.services.async_call(
                "media_player",
                "media_stop",
                {"entity_id": self._media_player}
            )
        
        # Turn off all indicator lights
        for light in self._indicator_lights:
            await self.hass.services.async_call(
                "light",
                "turn_off",
                {"entity_id": light}
            )
        
        self._state = AlarmControlPanelState.DISARMED
        self.async_write_ha_state()
        
        # Visual feedback - green
        await self._set_light_color(COLOR_GREEN, duration=1.0)
        
        await self._send_notification(
            "Alarm unscharf",
            "Per NFC deaktiviert."
        )

    @callback
    async def _handle_sensor_triggered(self, event):
        """Handle trigger sensor state change."""
        new_state = event.data.get("new_state")
        old_state = event.data.get("old_state")
        
        if new_state is None or new_state.state != "on":
            return
        
        if self._state != AlarmControlPanelState.ARMED_AWAY:
            return
        
        _LOGGER.info(f"Trigger sensor activated: {new_state.entity_id}")
        
        # Start entry delay
        self._state = AlarmControlPanelState.PENDING
        self.async_write_ha_state()
        
        # Visual feedback - orange
        await self._set_light_color(COLOR_ORANGE, brightness=100)
        
        await self._send_notification(
            "Vor-Alarm: Zutritt erkannt",
            f"Bitte NFC-Tag innerhalb {self._entry_delay} s scannen.",
            priority="high"
        )
        
        # Wait for entry delay
        try:
            await asyncio.sleep(self._entry_delay)
            
            # If we get here, alarm was not disarmed
            await self._trigger_alarm()
            
        except asyncio.CancelledError:
            _LOGGER.debug("Entry delay cancelled - alarm disarmed")

    async def _trigger_alarm(self):
        """Trigger the alarm."""
        self._state = AlarmControlPanelState.TRIGGERED
        self.async_write_ha_state()
        
        await self._send_notification(
            "🟥 ALARM AUSGELÖST",
            "Zutritt erkannt und nicht entschärft.",
            priority="high"
        )
        
        # Start siren
        if self._enable_siren and self._media_player and self._siren_file:
            await self._play_siren()
        
        # Start red light pulsing
        asyncio.create_task(self._pulse_red_lights())

    async def _play_siren(self):
        """Play the siren sound."""
        try:
            # Set volume to maximum
            await self.hass.services.async_call(
                "media_player",
                "volume_set",
                {
                    "entity_id": self._media_player,
                    "volume_level": 1.0
                }
            )
            
            await asyncio.sleep(0.5)
            
            # Play siren file
            await self.hass.services.async_call(
                "media_player",
                "play_media",
                {
                    "entity_id": self._media_player,
                    "media_content_id": self._siren_file,
                    "media_content_type": "music"
                }
            )
        except Exception as e:
            _LOGGER.error(f"Error playing siren: {e}")

    async def _pulse_red_lights(self):
        """Pulse red lights while alarm is triggered."""
        pulse_count = 0
        max_pulses = 15
        
        while self._state == AlarmControlPanelState.TRIGGERED and pulse_count < max_pulses:
            # Turn on red
            for light in self._indicator_lights:
                await self.hass.services.async_call(
                    "light",
                    "turn_on",
                    {
                        "entity_id": light,
                        "brightness_pct": 100,
                        "rgb_color": [255, 0, 0],
                        "transition": 0
                    }
                )
            
            await asyncio.sleep(1)
            
            # Turn off
            for light in self._indicator_lights:
                await self.hass.services.async_call(
                    "light",
                    "turn_off",
                    {
                        "entity_id": light,
                        "transition": 0
                    }
                )
            
            await asyncio.sleep(1)
            pulse_count += 1

    async def _blink_lights(self, color: str, count: int):
        """Blink indicator lights."""
        color_map = {
            COLOR_GREEN: [0, 255, 0],
            COLOR_YELLOW: [255, 255, 0],
            COLOR_ORANGE: [255, 165, 0],
            COLOR_BLUE: [0, 0, 255],
            COLOR_RED: [255, 0, 0],
        }
        
        rgb = color_map.get(color, [255, 255, 255])
        
        for _ in range(count):
            for light in self._indicator_lights:
                await self.hass.services.async_call(
                    "light",
                    "turn_on",
                    {
                        "entity_id": light,
                        "brightness_pct": 100,
                        "rgb_color": rgb
                    }
                )
            
            await asyncio.sleep(0.3)
            
            for light in self._indicator_lights:
                await self.hass.services.async_call(
                    "light",
                    "turn_off",
                    {"entity_id": light}
                )
            
            await asyncio.sleep(0.2)

    async def _set_light_color(self, color: str, brightness: int = 100, duration: float = 1.0):
        """Set indicator lights to a specific color."""
        color_map = {
            COLOR_GREEN: [0, 255, 0],
            COLOR_YELLOW: [255, 255, 0],
            COLOR_ORANGE: [255, 165, 0],
            COLOR_BLUE: [0, 0, 255],
            COLOR_RED: [255, 0, 0],
        }
        
        rgb = color_map.get(color, [255, 255, 255])
        
        for light in self._indicator_lights:
            await self.hass.services.async_call(
                "light",
                "turn_on",
                {
                    "entity_id": light,
                    "brightness_pct": brightness,
                    "rgb_color": rgb
                }
            )
        
        await asyncio.sleep(duration)
        
        for light in self._indicator_lights:
            await self.hass.services.async_call(
                "light",
                "turn_off",
                {"entity_id": light}
            )

    async def _send_notification(self, title: str, message: str, priority: str = "normal"):
        """Send notification if enabled."""
        if not self._enable_notifications or not self._notify_service:
            return
        
        try:
            service_parts = self._notify_service.split(".")
            if len(service_parts) == 2:
                domain, service = service_parts
                await self.hass.services.async_call(
                    domain,
                    service,
                    {
                        "title": title,
                        "message": message,
                        "data": {
                            "tag": "nfc_alarm_system",
                            "priority": priority
                        }
                    }
                )
        except Exception as e:
            _LOGGER.error(f"Error sending notification: {e}")

    async def async_alarm_disarm(self, code=None):
        """Send disarm command."""
        await self._disarm_sequence()

    async def async_alarm_arm_away(self, code=None):
        """Send arm away command."""
        if self._state == AlarmControlPanelState.DISARMED:
            self._arming_task = asyncio.create_task(self._start_arming_sequence())

    @property
    def state(self):
        """Return the state of the alarm."""
        return self._state

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": self._attr_name,
            "manufacturer": "NFC Alarm System",
            "model": "Custom Integration",
            "sw_version": "1.0.0",
        }
