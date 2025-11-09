# HA Alarm Lite (v0.5.0)

Small custom integration for Home Assistant that gives you a simple, robust alarm system with NFC disarm, exit/entry delays, light feedback and a local MP3 siren.

## Features
- Arm (exit delay), Entry delay, Trigger
- Disarm by NFC tag or from the panel
- Indicator light blink patterns (arming/armed/alarm)
- Play local MP3 on your media player
- Auto disarm at a daily time
- Health check + diagnostics
- Ready-made dashboard view

## Install (HACS custom repository)
1. Make this repo public and add it to HACS → Custom repositories (type **Integration**).
2. Install **HA Alarm Lite** and restart Home Assistant.
3. Go to **Settings → Devices & Services → Add Integration → HA Alarm Lite** and complete the setup.

### Setup tips
- **MP3 file**: picker lists files discovered under `/media` and `/config/www` (converted to `media-source://` automatically).
- **NFC tag**: dropdown shows tags from the HA Tag Manager (scan a tag once to register it).

## Dashboard
A prebuilt Lovelace view is included:

**File:** `custom_components/ha_alarm_lite/dashboard/ha_alarm_lite_dashboard.yaml`

Add to your dashboard:
1. Open your Dashboard → **Edit** → **Raw configuration editor**.
2. Add under `views:`:
   ```yaml
   - !include /config/custom_components/ha_alarm_lite/dashboard/ha_alarm_lite_dashboard.yaml
   ```
3. Save.  
4. Replace placeholders in the *Sensors & Devices* card (or just edit via UI):
   - Replace `[[indicator_light]]` with your indicator light entity id.
   - Replace `[[siren_player]]` with your media_player entity id.

## Services
- `ha_alarm_lite.health_check`
- `ha_alarm_lite.test_indicator`
- `ha_alarm_lite.test_siren`
- `ha_alarm_lite.ack_alarm`

## Entity
- `alarm_control_panel.ha_alarm_lite`

MIT licensed.


### Panel-Style View
If you prefer a compact panel like in the examples, include:
```yaml
- !include /config/custom_components/ha_alarm_lite/dashboard/ha_alarm_lite_panel.yaml
```
Then replace the placeholders:
- `[[sensor_1]]`, `[[sensor_2]]` → your entry sensors
- `[[indicator_light]]` → your indicator light

## v0.5.2
- Fix: MP3 path handling is lenient (accepts `media/...`, `/media/...`, `local/...`, `/local/...`, full `media-source://` and `http(s)://`).
- If an unknown format is given, setup no longer fails; siren playback is simply skipped.
