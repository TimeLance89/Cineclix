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
    CONF_SIREN_VOLUME,
    CONF_EXIT_DELAY,
    CONF_ENTRY_DELAY,
    CONF_AUTO_DISARM_TIME,
    CONF_ENABLE_AUTO_DISARM,
    CONF_NOTIFY_SERVICE,
    CONF_ENABLE_NOTIFICATIONS,
    DEFAULT_EXIT_DELAY,
    DEFAULT_ENTRY_DELAY,
    DEFAULT_AUTO_DISARM_TIME,
    DEFAULT_SIREN_VOLUME,
)

_LOGGER = logging.getLogger(__name__)


class NFCAlarmSystemConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NFC Alarm System."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self.basic_config = {}
        self.nfc_config = {}
        self.timing_config = {}
        self.media_config = {}
        self.notification_config = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial step - Welcome and basic setup."""
        errors = {}

        if user_input is not None:
            # Validate name is not empty
            if not user_input.get(CONF_NAME, "").strip():
                errors["base"] = "name_required"
            else:
                self.basic_config = user_input
                return await self.async_step_devices()

        data_schema = vol.Schema({
            vol.Required(CONF_NAME, default="NFC Alarmsystem"): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "step": "1/6",
                "info": "Willkommen beim Setup-Assistenten! Geben Sie Ihrem Alarmsystem einen eindeutigen Namen."
            }
        )

    async def async_step_devices(self, user_input=None):
        """Handle device selection - lights and sensors."""
        errors = {}

        if user_input is not None:
            # Validate at least one light and one sensor
            if not user_input.get(CONF_INDICATOR_LIGHTS):
                errors["base"] = "no_lights"
            elif not user_input.get(CONF_TRIGGER_SENSORS):
                errors["base"] = "no_sensors"
            else:
                self.basic_config.update(user_input)
                return await self.async_step_timing()

        data_schema = vol.Schema({
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
        })

        return self.async_show_form(
            step_id="devices",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "step": "2/6",
                "info": "Wählen Sie die Geräte für Ihr Alarmsystem:\n\n💡 Indikator-Lichter zeigen den Status (grün=aus, gelb=aktivierung, blau=scharf, orange=verzögerung, rot=alarm)\n\n🚪 Auslöser-Sensoren lösen den Alarm aus (z.B. Tür-/Fenstersensoren)"
            }
        )

    async def async_step_timing(self, user_input=None):
        """Handle timing configuration."""
        errors = {}

        if user_input is not None:
            self.timing_config = user_input
            return await self.async_step_nfc_tags()

        data_schema = vol.Schema({
            vol.Required(CONF_EXIT_DELAY, default=DEFAULT_EXIT_DELAY): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=600,
                    step=5,
                    unit_of_measurement="Sekunden",
                    mode=selector.NumberSelectorMode.SLIDER
                )
            ),
            vol.Required(CONF_ENTRY_DELAY, default=DEFAULT_ENTRY_DELAY): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=300,
                    step=5,
                    unit_of_measurement="Sekunden",
                    mode=selector.NumberSelectorMode.SLIDER
                )
            ),
        })

        return self.async_show_form(
            step_id="timing",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "step": "3/6",
                "info": "Konfigurieren Sie die Verzögerungszeiten:\n\n⏱️ Austrittsverzögerung: Zeit zum Verlassen nach dem Scharfschalten\n\n⏱️ Eintrittsverzögerung: Zeit zum Unscharfschalten nach Auslösung eines Sensors"
            }
        )

    async def async_step_nfc_tags(self, user_input=None):
        """Handle NFC tag configuration."""
        errors = {}

        if user_input is not None:
            # Validate tag IDs
            arm_tag = user_input.get(CONF_ARM_TAG, "").strip()
            disarm_tag = user_input.get(CONF_DISARM_TAG, "").strip()
            use_single = user_input.get(CONF_USE_SINGLE_TAG, True)
            
            if not arm_tag:
                errors["base"] = "arm_tag_required"
            elif not use_single and not disarm_tag:
                errors["base"] = "disarm_tag_required"
            else:
                self.nfc_config = user_input
                return await self.async_step_media()

        data_schema = vol.Schema({
            vol.Required(CONF_USE_SINGLE_TAG, default=True): selector.BooleanSelector(),
            vol.Required(CONF_ARM_TAG, default=""): selector.TextSelector(
                selector.TextSelectorConfig(
                    multiline=False,
                    type=selector.TextSelectorType.TEXT
                )
            ),
            vol.Optional(CONF_DISARM_TAG, default=""): selector.TextSelector(
                selector.TextSelectorConfig(
                    multiline=False,
                    type=selector.TextSelectorType.TEXT
                )
            ),
        })

        return self.async_show_form(
            step_id="nfc_tags",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "step": "4/6",
                "info": "Konfigurieren Sie Ihre NFC-Tags:\n\n🏷️ Ein Tag für beide: Verwenden Sie denselben Tag zum Scharf- und Unscharfschalten\n\n🏷️ Separate Tags: Verwenden Sie unterschiedliche Tags für Scharf- und Unscharfschalten\n\n💡 Tipp: Scannen Sie einen Tag und finden Sie die ID unter Entwicklerwerkzeuge → Ereignisse → tag_scanned"
            }
        )

    async def async_step_media(self, user_input=None):
        """Handle media player and siren configuration."""
        errors = {}

        if user_input is not None:
            enable_siren = user_input.get(CONF_ENABLE_SIREN, False)
            
            # Validate siren configuration if enabled
            if enable_siren:
                if not user_input.get(CONF_MEDIA_PLAYER):
                    errors["base"] = "media_player_required"
                elif not user_input.get(CONF_SIREN_FILE, "").strip():
                    errors["base"] = "siren_file_required"
            
            if not errors:
                self.media_config = user_input
                return await self.async_step_notifications()

        data_schema = vol.Schema({
            vol.Required(CONF_ENABLE_SIREN, default=False): selector.BooleanSelector(),
            vol.Optional(CONF_MEDIA_PLAYER): selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain="media_player",
                    multiple=False
                )
            ),
            vol.Optional(CONF_SIREN_FILE, default=""): selector.TextSelector(
                selector.TextSelectorConfig(
                    multiline=False,
                    type=selector.TextSelectorType.TEXT
                )
            ),
            vol.Optional(CONF_SIREN_VOLUME, default=DEFAULT_SIREN_VOLUME): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0.0,
                    max=1.0,
                    step=0.05,
                    mode=selector.NumberSelectorMode.SLIDER
                )
            ),
        })

        return self.async_show_form(
            step_id="media",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "step": "5/6",
                "info": "Sirenen-Konfiguration (optional):\n\n🔊 Aktivieren Sie die Sirene, um bei Alarm eine Audiodatei abzuspielen\n\n📱 Wählen Sie einen Media Player (z.B. Google Nest, Sonos)\n\n🎵 Dateipfad-Beispiel: media-source://media_source/local/siren.mp3\n\n💡 Tipp: Laden Sie die Audiodatei in /config/www/ oder /media/ hoch"
            }
        )

    async def async_step_notifications(self, user_input=None):
        """Handle notification and automation configuration."""
        errors = {}

        if user_input is not None:
            enable_notifications = user_input.get(CONF_ENABLE_NOTIFICATIONS, False)
            enable_auto_disarm = user_input.get(CONF_ENABLE_AUTO_DISARM, False)
            
            # Validate notification service if enabled
            if enable_notifications and not user_input.get(CONF_NOTIFY_SERVICE, "").strip():
                errors["base"] = "notify_service_required"
            
            # Validate auto disarm time if enabled
            if enable_auto_disarm and not user_input.get(CONF_AUTO_DISARM_TIME):
                errors["base"] = "auto_disarm_time_required"
            
            if not errors:
                self.notification_config = user_input
                
                # Combine all configurations
                final_config = {
                    **self.basic_config,
                    **self.timing_config,
                    **self.nfc_config,
                    **self.media_config,
                    **self.notification_config
                }
                
                # Create the config entry
                return self.async_create_entry(
                    title=final_config[CONF_NAME],
                    data=final_config
                )

        data_schema = vol.Schema({
            vol.Required(CONF_ENABLE_NOTIFICATIONS, default=False): selector.BooleanSelector(),
            vol.Optional(CONF_NOTIFY_SERVICE, default=""): selector.TextSelector(
                selector.TextSelectorConfig(
                    multiline=False,
                    type=selector.TextSelectorType.TEXT
                )
            ),
            vol.Required(CONF_ENABLE_AUTO_DISARM, default=False): selector.BooleanSelector(),
            vol.Optional(CONF_AUTO_DISARM_TIME, default=DEFAULT_AUTO_DISARM_TIME): selector.TimeSelector(),
        })

        return self.async_show_form(
            step_id="notifications",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "step": "6/6",
                "info": "Benachrichtigungen & Automatisierung (optional):\n\n📲 Benachrichtigungen: Erhalten Sie Push-Nachrichten bei Statusänderungen\n\n🔔 Service-Beispiel: notify.mobile_app_iphone\n\n⏰ Auto-Unscharfschaltung: Schalten Sie das Alarmsystem täglich zu einer bestimmten Zeit automatisch unscharf\n\n💡 Tipp: Testen Sie den Benachrichtigungs-Service unter Entwicklerwerkzeuge → Dienste"
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
        """Manage the options - main menu."""
        if user_input is not None:
            option = user_input.get("option")
            if option == "timing":
                return await self.async_step_timing()
            elif option == "nfc_tags":
                return await self.async_step_nfc_tags()
            elif option == "media":
                return await self.async_step_media()
            elif option == "notifications":
                return await self.async_step_notifications()

        data_schema = vol.Schema({
            vol.Required("option"): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        {"label": "⏱️ Verzögerungszeiten", "value": "timing"},
                        {"label": "🏷️ NFC-Tags", "value": "nfc_tags"},
                        {"label": "🔊 Sirene & Medien", "value": "media"},
                        {"label": "📲 Benachrichtigungen", "value": "notifications"},
                    ],
                    mode=selector.SelectSelectorMode.LIST
                )
            )
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            description_placeholders={
                "info": "Wählen Sie die Einstellung, die Sie ändern möchten:"
            }
        )

    async def async_step_timing(self, user_input=None):
        """Handle timing options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Required(
                CONF_EXIT_DELAY,
                default=self.config_entry.data.get(CONF_EXIT_DELAY, DEFAULT_EXIT_DELAY)
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=600,
                    step=5,
                    unit_of_measurement="Sekunden",
                    mode=selector.NumberSelectorMode.SLIDER
                )
            ),
            vol.Required(
                CONF_ENTRY_DELAY,
                default=self.config_entry.data.get(CONF_ENTRY_DELAY, DEFAULT_ENTRY_DELAY)
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0,
                    max=300,
                    step=5,
                    unit_of_measurement="Sekunden",
                    mode=selector.NumberSelectorMode.SLIDER
                )
            ),
        })

        return self.async_show_form(
            step_id="timing",
            data_schema=data_schema,
            description_placeholders={
                "info": "Passen Sie die Verzögerungszeiten an:\n\n⏱️ Austrittsverzögerung: Zeit zum Verlassen\n⏱️ Eintrittsverzögerung: Zeit zum Unscharfschalten"
            }
        )

    async def async_step_nfc_tags(self, user_input=None):
        """Handle NFC tag options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Required(
                CONF_USE_SINGLE_TAG,
                default=self.config_entry.data.get(CONF_USE_SINGLE_TAG, True)
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_ARM_TAG,
                default=self.config_entry.data.get(CONF_ARM_TAG, "")
            ): selector.TextSelector(),
            vol.Optional(
                CONF_DISARM_TAG,
                default=self.config_entry.data.get(CONF_DISARM_TAG, "")
            ): selector.TextSelector(),
        })

        return self.async_show_form(
            step_id="nfc_tags",
            data_schema=data_schema,
            description_placeholders={
                "info": "Aktualisieren Sie Ihre NFC-Tag-Konfiguration"
            }
        )

    async def async_step_media(self, user_input=None):
        """Handle media options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Required(
                CONF_ENABLE_SIREN,
                default=self.config_entry.data.get(CONF_ENABLE_SIREN, False)
            ): selector.BooleanSelector(),
            vol.Optional(
                CONF_MEDIA_PLAYER,
                default=self.config_entry.data.get(CONF_MEDIA_PLAYER)
            ): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="media_player")
            ),
            vol.Optional(
                CONF_SIREN_FILE,
                default=self.config_entry.data.get(CONF_SIREN_FILE, "")
            ): selector.TextSelector(),
            vol.Optional(
                CONF_SIREN_VOLUME,
                default=self.config_entry.data.get(CONF_SIREN_VOLUME, DEFAULT_SIREN_VOLUME)
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=0.0, max=1.0, step=0.05, mode=selector.NumberSelectorMode.SLIDER
                )
            ),
        })

        return self.async_show_form(
            step_id="media",
            data_schema=data_schema,
            description_placeholders={
                "info": "Aktualisieren Sie Ihre Sirenen-Konfiguration"
            }
        )

    async def async_step_notifications(self, user_input=None):
        """Handle notification options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Required(
                CONF_ENABLE_NOTIFICATIONS,
                default=self.config_entry.data.get(CONF_ENABLE_NOTIFICATIONS, False)
            ): selector.BooleanSelector(),
            vol.Optional(
                CONF_NOTIFY_SERVICE,
                default=self.config_entry.data.get(CONF_NOTIFY_SERVICE, "")
            ): selector.TextSelector(),
            vol.Required(
                CONF_ENABLE_AUTO_DISARM,
                default=self.config_entry.data.get(CONF_ENABLE_AUTO_DISARM, False)
            ): selector.BooleanSelector(),
            vol.Optional(
                CONF_AUTO_DISARM_TIME,
                default=self.config_entry.data.get(CONF_AUTO_DISARM_TIME, DEFAULT_AUTO_DISARM_TIME)
            ): selector.TimeSelector(),
        })

        return self.async_show_form(
            step_id="notifications",
            data_schema=data_schema,
            description_placeholders={
                "info": "Aktualisieren Sie Ihre Benachrichtigungs-Einstellungen"
            }
        )
