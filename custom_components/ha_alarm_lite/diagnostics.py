from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, DATA_CTRL

async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry):
    ctrl = hass.data.get(DOMAIN, {}).get(entry.entry_id, {}).get(DATA_CTRL)
    if not ctrl:
        return {"state": "unknown"}
    return {
        "state": getattr(ctrl, "_state", "unknown"),
        "options": entry.options,
    }
