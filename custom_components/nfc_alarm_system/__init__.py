"""NFC Alarm System Integration für Home Assistant."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

_LOGGER = logging.getLogger(__name__)

DOMAIN = "nfc_alarm_system"
PLATFORMS = [Platform.ALARM_CONTROL_PANEL]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NFC Alarm System from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Register event listener for NFC tags
    async def handle_tag_scanned(event):
        """Handle tag scanned event."""
        _LOGGER.debug(f"Tag scanned: {event.data}")
        # The alarm panel will handle this
    
    hass.bus.async_listen("tag_scanned", handle_tag_scanned)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok
