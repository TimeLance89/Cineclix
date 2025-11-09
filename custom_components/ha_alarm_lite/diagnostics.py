from __future__ import annotations
from datetime import datetime
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry):
    ent_id = "alarm_control_panel.ha_alarm_lite"
    st = hass.states.get(ent_id)
    data = {
        "entry_id": entry.entry_id,
        "options": dict(entry.options),
        "entity_state": st.state if st else None,
        "entity_attrs": dict(st.attributes) if st else None,
        "time": datetime.utcnow().isoformat(),
    }
    return data