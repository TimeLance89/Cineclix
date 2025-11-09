"""HA Alarm Lite - backend bootstrap."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "ha_alarm_lite"
PLATFORMS: list[str] = []  # No entity platforms for now

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "options": dict(entry.options),
        "data": dict(entry.data),
    }
    # Watch for option changes
    entry.async_on_unload(entry.add_update_listener(async_update_listener))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return True

async def async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update by reloading the entry."""
    await hass.config_entries.async_reload(entry.entry_id)
