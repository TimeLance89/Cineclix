"""Config flow for NFC Alarm System."""
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.const import CONF_NAME

from .const import (
    DOMAIN,
    CONF_INDICATOR_LIGHTS,
    CONF_TRIGGER_SENSORS,
    CONF_NFC_TAGS,
    CONF_USE_SINGLE_TAG,
    CONF_ARM_TAG,
    CONF_DISARM_TAG,
    CONF_MEDIA_PLAYER,
    CONF_SIREN_FILE,
    CONF_ENABLE_SIREN,
    CONF_EXIT_DELAY,
    CONF_ENTRY_DELAY,
    CONF_AUTO_DISARM_TIME,
    CONF_ENABLE_AUTO_DISARM,
    CONF_NOTIFY_SERVICE,
    CONF_ENABLE_NOTIFICATIONS,
    DEFAULT_EXIT_DELAY,
    DEFAULT_ENTRY_DELAY,
    DEFAULT_AUTO_DISARM_TIME,
)

_LOGGER = logging.getLogger(__name__)


class NFCAlarmSystemConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NFC Alarm System."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step - Basic configuration."""
        errors = {}

        if user_input is not None:
            # Store basic config and move to next step
            self.basic_config = user_input
            return await self.async_step_nfc_tags()

        data_schema = vol.Schema({
            vol.Required(CONF_NAME, default="NFC Alarmsystem"): str,
            vol.Required(CONF_INDICATOR_LIGHTS): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain="light",
                    multiple=True
                )
            ),
            vol.Required(CONF_TRIGGER_SENSORS): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain="binary_sensor",
                    multiple=True
                )
            ),
            vol.Required(CONF_EXIT_DELAY, default=DEFAULT_EXIT_DELAY): vol.All(
                vol.Coerce(int), vol.Range(min=0, max=600)
            ),
            vol.Required(CONF_ENTRY_DELAY, default=DEFAULT_ENTRY_DELAY): vol.All(
                vol.Coerce(int), vol.Range(min=0, max=300)
            ),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "name": "Grundkonfiguration"
            }
        )

    async def async_step_nfc_tags(self, user_input=None):
        """Handle NFC tag configuration."""
        errors = {}

        if user_input is not None:
            self.nfc_config = user_input
            return await self.async_step_media()

        data_schema = vol.Schema({
            vol.Required(CONF_USE_SINGLE_TAG, default=True): bool,
            vol.Required(CONF_ARM_TAG, default=""): str,
            vol.Optional(CONF_DISARM_TAG, default=""): str,
        })

        return self.async_show_form(
            step_id="nfc_tags",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "info": "Geben Sie die NFC-Tag-IDs ein. Bei 'Ein Tag für beide' wird nur der Scharf-Tag verwendet."
            }
        )

    async def async_step_media(self, user_input=None):
        """Handle media player and siren configuration."""
        errors = {}

        if user_input is not None:
            self.media_config = user_input
            return await self.async_step_notifications()

        data_schema = vol.Schema({
            vol.Required(CONF_ENABLE_SIREN, default=False): bool,
            vol.Optional(CONF_MEDIA_PLAYER): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain="media_player",
                    multiple=False
                )
            ),
            vol.Optional(CONF_SIREN_FILE, default=""): selector.TextSelector(
                selector.TextSelectorConfig(
                    multiline=False
                )
            ),
        })

        return self.async_show_form(
            step_id="media",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "info": "Sirene ist optional. Beispiel Pfad: media-source://media_source/local/siren.mp3"
            }
        )

    async def async_step_notifications(self, user_input=None):
        """Handle notification configuration."""
        errors = {}

        if user_input is not None:
            # Combine all configurations
            final_config = {
                **self.basic_config,
                **self.nfc_config,
                **self.media_config,
                **user_input
            }
            
            # Create the config entry
            return self.async_create_entry(
                title=final_config[CONF_NAME],
                data=final_config
            )

        data_schema = vol.Schema({
            vol.Required(CONF_ENABLE_NOTIFICATIONS, default=False): bool,
            vol.Optional(CONF_NOTIFY_SERVICE, default=""): str,
            vol.Required(CONF_ENABLE_AUTO_DISARM, default=False): bool,
            vol.Optional(CONF_AUTO_DISARM_TIME, default=DEFAULT_AUTO_DISARM_TIME): selector.TimeSelector(),
        })

        return self.async_show_form(
            step_id="notifications",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "info": "Benachrichtigungen sind optional. Beispiel Service: notify.mobile_app_device_name"
            }
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return NFCAlarmSystemOptionsFlow(config_entry)


class NFCAlarmSystemOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for NFC Alarm System."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    CONF_EXIT_DELAY,
                    default=self.config_entry.data.get(CONF_EXIT_DELAY, DEFAULT_EXIT_DELAY)
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=600)),
                vol.Required(
                    CONF_ENTRY_DELAY,
                    default=self.config_entry.data.get(CONF_ENTRY_DELAY, DEFAULT_ENTRY_DELAY)
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=300)),
            })
        )
