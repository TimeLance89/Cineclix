
from __future__ import annotations

DOMAIN = "ha_alarm_pro"

CONF_INDICATOR_LIGHT = "indicator_light"
CONF_SIREN_PLAYER = "siren_player"
CONF_SIREN_VOLUME = "siren_volume"
CONF_MP3_FILE = "mp3_file"
CONF_ENTRY_SENSORS = "entry_sensors"
CONF_NFC_TAG = "nfc_tag"
CONF_ALLOW_ANY_TAG = "allow_any_tag"
CONF_ACCEPT_ANY_TAG_WHEN_TRIGGERED = "allow_any_when_triggered"
CONF_EXIT_DELAY = "exit_delay"
CONF_ENTRY_DELAY = "entry_delay"
CONF_AUTO_DISARM_TIME = "auto_disarm_time"

DEFAULT_EXIT_DELAY = 30
DEFAULT_ENTRY_DELAY = 30
DEFAULT_VOLUME = 1

EVENT_ENTRY_DELAY_STARTED = f"{DOMAIN}_entry_delay_started"
EVENT_ENTRY_DELAY_CANCELLED = f"{DOMAIN}_entry_delay_cancelled"
