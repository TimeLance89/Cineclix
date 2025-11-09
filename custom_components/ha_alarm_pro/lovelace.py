"""Dynamic Lovelace dashboard generator for HA Alarm Pro."""
from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN, CONF_ENTRY_SENSORS, CONF_INDICATOR_LIGHT


def generate_dashboard_config(hass: HomeAssistant, entry_id: str) -> dict[str, Any]:
    """Generate a dynamic dashboard configuration based on the integration config."""
    
    # Get the config entry
    entry = hass.config_entries.async_get_entry(entry_id)
    if not entry:
        return _get_fallback_config()
    
    config = entry.options or entry.data
    
    # Build the dashboard
    dashboard = {
        "type": "vertical-stack",
        "cards": []
    }
    
    # Add conditional alarm warning
    dashboard["cards"].append(_build_alarm_warning())
    
    # Add status card
    dashboard["cards"].append(_build_status_card())
    
    # Add control buttons
    dashboard["cards"].extend(_build_control_buttons())
    
    # Add sensors and lights card (dynamically populated)
    sensors_card = _build_sensors_card(config)
    if sensors_card:
        dashboard["cards"].append(sensors_card)
    
    # Add logbook
    dashboard["cards"].append(_build_logbook(config))
    
    return dashboard


def _build_alarm_warning() -> dict[str, Any]:
    """Build the conditional alarm warning card."""
    return {
        "type": "conditional",
        "conditions": [
            {
                "entity": "alarm_control_panel.ha_alarm_pro",
                "state": "triggered"
            }
        ],
        "card": {
            "type": "markdown",
            "content": "## 🔴 ALARM AUSGELÖST\nQuittiere den Alarm mit **\"Alarm quittieren\"** oder per NFC-Tag."
        }
    }


def _build_status_card() -> dict[str, Any]:
    """Build the status entities card."""
    return {
        "type": "entities",
        "title": "Alarm-Status",
        "show_header_toggle": False,
        "state_color": True,
        "entities": [
            {
                "entity": "alarm_control_panel.ha_alarm_pro",
                "name": "Alarmanlage",
                "secondary_info": "last-changed"
            },
            {
                "type": "attribute",
                "entity": "alarm_control_panel.ha_alarm_pro",
                "attribute": "entry_delay_active",
                "name": "Eintrittsverzögerung aktiv",
                "icon": "mdi:timer-sand"
            },
            {
                "type": "attribute",
                "entity": "alarm_control_panel.ha_alarm_pro",
                "attribute": "last_trigger_source",
                "name": "Letzter Auslöser",
                "icon": "mdi:alert-decagram"
            },
            {
                "type": "attribute",
                "entity": "alarm_control_panel.ha_alarm_pro",
                "attribute": "last_disarm_tag",
                "name": "Letzter NFC-Tag",
                "icon": "mdi:nfc"
            }
        ]
    }


def _build_control_buttons() -> list[dict[str, Any]]:
    """Build the control button rows."""
    return [
        {
            "type": "horizontal-stack",
            "cards": [
                {
                    "type": "button",
                    "name": "Scharf (Abwesend)",
                    "icon": "mdi:shield-lock",
                    "tap_action": {
                        "action": "call-service",
                        "service": "alarm_control_panel.alarm_arm_away",
                        "target": {
                            "entity_id": "alarm_control_panel.ha_alarm_pro"
                        }
                    },
                    "entity": "alarm_control_panel.ha_alarm_pro",
                    "show_state": False
                },
                {
                    "type": "button",
                    "name": "Scharf (Zuhause)",
                    "icon": "mdi:shield-home",
                    "tap_action": {
                        "action": "call-service",
                        "service": "alarm_control_panel.alarm_arm_home",
                        "target": {
                            "entity_id": "alarm_control_panel.ha_alarm_pro"
                        }
                    },
                    "entity": "alarm_control_panel.ha_alarm_pro",
                    "show_state": False
                }
            ]
        },
        {
            "type": "horizontal-stack",
            "cards": [
                {
                    "type": "button",
                    "name": "Unscharf",
                    "icon": "mdi:shield-off",
                    "tap_action": {
                        "action": "call-service",
                        "service": "alarm_control_panel.alarm_disarm",
                        "target": {
                            "entity_id": "alarm_control_panel.ha_alarm_pro"
                        }
                    },
                    "entity": "alarm_control_panel.ha_alarm_pro",
                    "show_state": False
                },
                {
                    "type": "button",
                    "name": "Alarm testen",
                    "icon": "mdi:alarm-light",
                    "tap_action": {
                        "action": "call-service",
                        "service": "ha_alarm_pro.test_alarm",
                        "target": {
                            "entity_id": "alarm_control_panel.ha_alarm_pro"
                        }
                    },
                    "entity": "alarm_control_panel.ha_alarm_pro",
                    "show_state": False
                },
                {
                    "type": "button",
                    "name": "Alarm quittieren",
                    "icon": "mdi:bell-cancel",
                    "tap_action": {
                        "action": "call-service",
                        "service": "alarm_control_panel.alarm_disarm",
                        "target": {
                            "entity_id": "alarm_control_panel.ha_alarm_pro"
                        }
                    },
                    "entity": "alarm_control_panel.ha_alarm_pro",
                    "show_state": False
                },
                {
                    "type": "button",
                    "name": "Sound testen",
                    "icon": "mdi:volume-high",
                    "tap_action": {
                        "action": "call-service",
                        "service": "ha_alarm_pro.test_alarm_sound",
                        "target": {
                            "entity_id": "alarm_control_panel.ha_alarm_pro"
                        }
                    },
                    "entity": "alarm_control_panel.ha_alarm_pro",
                    "show_state": False
                }
            ]
        }
    ]


def _build_sensors_card(config: dict[str, Any]) -> dict[str, Any] | None:
    """Build the sensors and lights card with configured entities."""
    entities = []
    
    # Add configured sensors
    sensors = config.get(CONF_ENTRY_SENSORS, [])
    if isinstance(sensors, str):
        sensors = [sensors]
    
    for sensor in sensors:
        if sensor:
            entities.append({
                "entity": sensor,
                "name": _get_friendly_name(sensor)
            })
    
    # Add divider if we have sensors and lights
    lights = config.get(CONF_INDICATOR_LIGHT, [])
    if isinstance(lights, str):
        lights = [lights]
    
    if entities and lights:
        entities.append({"type": "divider"})
    
    # Add configured lights
    for light in lights:
        if light:
            entities.append({
                "entity": light,
                "name": _get_friendly_name(light)
            })
    
    # Only return card if we have entities
    if not entities:
        return None
    
    return {
        "type": "entities",
        "title": "Sensoren & Indikatoren",
        "show_header_toggle": False,
        "state_color": True,
        "entities": entities
    }


def _build_logbook(config: dict[str, Any]) -> dict[str, Any]:
    """Build the logbook card with configured entities."""
    entities = ["alarm_control_panel.ha_alarm_pro"]
    
    # Add configured sensors
    sensors = config.get(CONF_ENTRY_SENSORS, [])
    if isinstance(sensors, str):
        sensors = [sensors]
    
    for sensor in sensors:
        if sensor:
            entities.append(sensor)
    
    return {
        "type": "logbook",
        "title": "Alarm-Historie (6 Stunden)",
        "hours_to_show": 6,
        "entities": entities
    }


def _get_friendly_name(entity_id: str) -> str:
    """Get a friendly name from entity_id."""
    # Extract the name part after the domain
    parts = entity_id.split(".")
    if len(parts) == 2:
        name = parts[1].replace("_", " ").title()
        return name
    return entity_id


def _get_fallback_config() -> dict[str, Any]:
    """Return a minimal fallback configuration."""
    return {
        "type": "entities",
        "title": "HA Alarm Pro",
        "entities": ["alarm_control_panel.ha_alarm_pro"]
    }
