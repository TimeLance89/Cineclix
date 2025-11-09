
DOMAIN = "ha_alarm_pro"
PLATFORMS: list[str] = ["alarm_control_panel"]

# Config keys
CONF_NAME = "name"
CONF_INDICATOR = "indicator_light"
CONF_MEDIA_PLAYER = "media_player"
CONF_VOLUME = "volume"
CONF_MP3 = "mp3_file"
CONF_SENSORS = "entry_sensors"
CONF_EXIT_DELAY = "exit_delay"
CONF_ENTRY_DELAY = "entry_delay"
CONF_ALLOW_ANY_TAG = "allow_any_tag"
CONF_NFC_TAG = "nfc_tag"
CONF_AUTO_DISARM = "auto_disarm_time"

DEFAULT_NAME = "HA Alarm Pro"
DEFAULT_EXIT_DELAY = 30
DEFAULT_ENTRY_DELAY = 30
DEFAULT_VOLUME = 1.0
