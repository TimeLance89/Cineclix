"""Panel component for HA Alarm Pro dashboard."""
from __future__ import annotations

import os
import yaml
from typing import Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.components import frontend
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, CONF_ENTRY_SENSORS, CONF_INDICATOR_LIGHT


async def async_register_panel(hass: HomeAssistant, entry_id: str) -> None:
    """Register the alarm panel in the frontend."""
    
    # Get the config entry
    entry = hass.config_entries.async_get_entry(entry_id)
    if not entry:
        return
    
    config = entry.options or entry.data
    
    # Build the dashboard configuration
    dashboard_config = await async_build_dashboard_config(hass, config)
    
    # Register the panel
    await hass.components.frontend.async_register_built_in_panel(
        component_name="lovelace",
        sidebar_title="Alarm Pro",
        sidebar_icon="mdi:shield-home",
        frontend_url_path="ha-alarm-pro",
        config={"mode": "yaml"},
        require_admin=False,
    )


async def async_build_dashboard_config(
    hass: HomeAssistant, config: dict[str, Any]
) -> dict[str, Any]:
    """Build the dashboard configuration based on user settings."""
    
    # Load base dashboard template
    dashboard_path = os.path.join(
        os.path.dirname(__file__), "dashboard", "alarm_panel.yaml"
    )
    
    try:
        with open(dashboard_path, "r", encoding="utf-8") as file:
            dashboard_config = yaml.safe_load(file)
    except Exception:
        # Fallback to basic config if file not found
        dashboard_config = _get_fallback_dashboard()
    
    # Customize based on configuration
    dashboard_config = _customize_dashboard(dashboard_config, config)
    
    return dashboard_config


def _customize_dashboard(
    dashboard_config: dict[str, Any], config: dict[str, Any]
) -> dict[str, Any]:
    """Customize the dashboard with user configuration."""
    
    # Find the sensors & lights card
    cards = dashboard_config.get("cards", [])
    
    for card in cards:
        if card.get("title") == "Sensoren & Indikatoren":
            entities = []
            
            # Add configured sensors
            sensors = config.get(CONF_ENTRY_SENSORS, [])
            if isinstance(sensors, list):
                for sensor in sensors:
                    entities.append({"entity": sensor, "name": sensor.split(".")[-1]})
            elif sensors:
                entities.append({"entity": sensors, "name": sensors.split(".")[-1]})
            
            # Add divider
            if entities:
                entities.append({"type": "divider"})
            
            # Add configured lights
            lights = config.get(CONF_INDICATOR_LIGHT, [])
            if isinstance(lights, list):
                for light in lights:
                    entities.append({"entity": light, "name": light.split(".")[-1]})
            elif lights:
                entities.append({"entity": lights, "name": lights.split(".")[-1]})
            
            card["entities"] = entities
        
        # Customize logbook
        elif card.get("type") == "logbook":
            entities = ["alarm_control_panel.ha_alarm_pro"]
            
            # Add sensors to logbook
            sensors = config.get(CONF_ENTRY_SENSORS, [])
            if isinstance(sensors, list):
                entities.extend(sensors)
            elif sensors:
                entities.append(sensors)
            
            card["entities"] = entities
    
    return dashboard_config


def _get_fallback_dashboard() -> dict[str, Any]:
    """Return a fallback dashboard configuration."""
    return {
        "type": "vertical-stack",
        "cards": [
            {
                "type": "entities",
                "title": "Alarm-Status",
                "entities": ["alarm_control_panel.ha_alarm_pro"],
            },
            {
                "type": "horizontal-stack",
                "cards": [
                    {
                        "type": "button",
                        "name": "Scharf",
                        "icon": "mdi:shield-lock",
                        "tap_action": {
                            "action": "call-service",
                            "service": "alarm_control_panel.alarm_arm_away",
                            "target": {"entity_id": "alarm_control_panel.ha_alarm_pro"},
                        },
                    },
                    {
                        "type": "button",
                        "name": "Unscharf",
                        "icon": "mdi:shield-off",
                        "tap_action": {
                            "action": "call-service",
                            "service": "alarm_control_panel.alarm_disarm",
                            "target": {"entity_id": "alarm_control_panel.ha_alarm_pro"},
                        },
                    },
                ],
            },
        ],
    }
