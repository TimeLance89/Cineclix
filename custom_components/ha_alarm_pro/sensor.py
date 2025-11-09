"""Sensor platform for HA Alarm Pro dashboard configuration."""
from __future__ import annotations

import json
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .lovelace import generate_dashboard_config


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the HA Alarm Pro dashboard sensor."""
    async_add_entities([AlarmProDashboardSensor(hass, entry)])


class AlarmProDashboardSensor(SensorEntity):
    """Sensor that provides the dashboard configuration."""

    _attr_has_entity_name = True
    _attr_name = "Dashboard Config"
    _attr_icon = "mdi:view-dashboard"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the dashboard sensor."""
        self.hass = hass
        self.entry = entry
        self._attr_unique_id = f"{DOMAIN}_dashboard_config"
        self._attr_native_value = "ready"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the dashboard configuration as attributes."""
        try:
            config = generate_dashboard_config(self.hass, self.entry.entry_id)
            return {
                "dashboard_config": json.dumps(config, indent=2),
                "config_yaml": self._config_to_yaml(config)
            }
        except Exception as e:
            return {
                "error": str(e),
                "dashboard_config": "{}",
                "config_yaml": ""
            }

    def _config_to_yaml(self, config: dict[str, Any]) -> str:
        """Convert config dict to YAML string."""
        import yaml
        try:
            return yaml.dump(config, default_flow_style=False, allow_unicode=True)
        except Exception:
            return ""

    async def async_update(self) -> None:
        """Update the sensor."""
        # Trigger state update
        self.async_write_ha_state()
