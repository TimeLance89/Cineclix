
from __future__ import annotations
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry):
    data = {**entry.data, **entry.options}
    # Hide secrets if any
    return {"options": data}
