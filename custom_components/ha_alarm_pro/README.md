
# HA Alarm Pro (v0.2.0)

A simple-but-solid custom alarm for Home Assistant:
- One **alarm_control_panel** entity
- Entry/exit delays
- Any number of entry sensors (binary_sensor) with entry delay handling
- Optional indicator light blink for arming, entry delay and alarm state
- Optional siren via media_player + MP3 (from `/media` or `/config/www`)
- NFC tag disarm (from HA Tag Manager) or allow any tag (including "any tag while triggered")
- Optional auto disarm at a specific time
- Lovelace panel snippet included in `dashboard/panel.yaml`

## Install (HACS custom repo or manual)
Copy `custom_components/ha_alarm_pro/` to your Home Assistant `/config/custom_components/` and restart.

## Add to UI
Add a *Manual card* and paste the YAML from `custom_components/ha_alarm_pro/dashboard/panel.yaml`.
