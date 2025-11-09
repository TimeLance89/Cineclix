# HA Alarm Lite (v0.6.0)

Custom integration for Home Assistant — easy setup, reliable alarm basics.

## What it does
- Select indicator light, siren/media player and volume
- Pick an MP3 from `/media` or `/config/www` (dropdown)
- Choose entry sensors (multi-select)
- Choose an NFC tag for arm/disarm (from the Tag Manager)
- Exit/entry delays and optional auto-disarm time
- Example Lovelace panel included: `custom_components/ha_alarm_lite/dashboard/panel.yaml`

## Install (manual quick test)
1. Copy `custom_components/ha_alarm_lite` into `/config/custom_components/`.
2. Restart Home Assistant.
3. Add the integration: **Settings → Devices & services → Add Integration → HA Alarm Lite**.
4. Configure options.
5. For the dashboard, add a *Manual card* and paste the YAML from `dashboard/panel.yaml`.
