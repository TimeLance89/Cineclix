
from __future__ import annotations
from typing import Any
from homeassistant.core import HomeAssistant
from homeassistant.components.diagnostics import async_redact_data
from .const import DOMAIN

TO_REDACT = set()

async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry):
    data = dict(entry.data)
    return async_redact_data(data, TO_REDACT)
