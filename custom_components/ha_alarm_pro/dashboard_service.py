"""Service for exporting dashboard configuration."""
from __future__ import annotations

import yaml
from typing import Any

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from .const import DOMAIN
from .lovelace import generate_dashboard_config


SERVICE_GET_DASHBOARD_YAML = "get_dashboard_yaml"

SERVICE_SCHEMA = vol.Schema({})


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for dashboard management."""

    async def handle_get_dashboard_yaml(call: ServiceCall) -> None:
        """Handle the get_dashboard_yaml service call."""
        # Get the first (and should be only) config entry
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            return

        entry = entries[0]
        config = generate_dashboard_config(hass, entry.entry_id)
        
        # Convert to YAML
        yaml_str = yaml.dump(config, default_flow_style=False, allow_unicode=True)
        
        # Send persistent notification with the YAML
        await hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": "HA Alarm Pro Dashboard YAML",
                "message": f"```yaml\n{yaml_str}\n```\n\nKopiere diesen Code in dein Dashboard.",
                "notification_id": "ha_alarm_pro_dashboard"
            }
        )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_DASHBOARD_YAML,
        handle_get_dashboard_yaml,
        schema=SERVICE_SCHEMA,
    )
