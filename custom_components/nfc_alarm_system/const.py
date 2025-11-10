"""Constants for NFC Alarm System."""

DOMAIN = "nfc_alarm_system"

# Configuration keys
CONF_INDICATOR_LIGHTS = "indicator_lights"
CONF_TRIGGER_SENSORS = "trigger_sensors"
CONF_NFC_TAGS = "nfc_tags"
CONF_USE_SINGLE_TAG = "use_single_tag"
CONF_ARM_TAG = "arm_tag"
CONF_DISARM_TAG = "disarm_tag"
CONF_MEDIA_PLAYER = "media_player"
CONF_SIREN_FILE = "siren_file"
CONF_ENABLE_SIREN = "enable_siren"
CONF_EXIT_DELAY = "exit_delay"
CONF_ENTRY_DELAY = "entry_delay"
CONF_AUTO_DISARM_TIME = "auto_disarm_time"
CONF_ENABLE_AUTO_DISARM = "enable_auto_disarm"
CONF_NOTIFY_SERVICE = "notify_service"
CONF_ENABLE_NOTIFICATIONS = "enable_notifications"

# Default values
DEFAULT_EXIT_DELAY = 120
DEFAULT_ENTRY_DELAY = 30
DEFAULT_AUTO_DISARM_TIME = "06:00:00"

# Color codes for indicator lights
COLOR_GREEN = "green"
COLOR_YELLOW = "yellow"
COLOR_ORANGE = "orange"
COLOR_BLUE = "blue"
COLOR_RED = "red"
