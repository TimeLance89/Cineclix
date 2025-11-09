
# HA Alarm Pro

A small but robust custom integration that turns Home Assistant into a **simple, reliable alarm system** — with NFC disarm, entry/exit delays, indicator light, and a siren played on any media player. Designed to be **easy to set up** (no YAML needed) and **fast to use** in daily life.

## Highlights
- **Alarm entity** (`alarm_control_panel`) with arm home/away, disarm, trigger
- **Entry/Exit delays** (visual blink on a light entity)
- **NFC disarm** (select a tag from HA Tag Manager or allow any tag)
- **Siren playback** on a chosen media player with **volume** and **MP3 file** (auto-lists files from `/media` and `/local`)
- **Optional auto-disarm** at a specific time
- Ready-to-use **Dashboard panel** (`dashboard/panel.yaml`)

## Installation (HACS – Custom Repository)
1. Make this repository **public** on GitHub.
2. In Home Assistant: **HACS → Integrations → Custom repositories → Add**  
   Repository: `https://github.com/<YOUR-USER>/ha-alarm-pro` – Type: **Integration**
3. Install **HA Alarm Pro**, then **Restart Home Assistant**.
4. Go to **Settings → Devices & Services → Add Integration → HA Alarm Pro** and complete the setup.

> Alternatively, drop `custom_components/ha_alarm_pro/` into `/config/custom_components/` and restart.

## Setup Tips
- **Indicator Light** (optional): a lamp that blinks during arming or alarm.
- **Siren / Media Player**: any supported media player (Nest Hub, Chromecast, etc.).
- **MP3 file**: the dropdown lists files from `/media` and `/config/www` (`/local`).  
  Put your siren under `/media/` or `/config/www/` and it appears automatically.
- **Entry Sensors**: choose one or more `binary_sensor` entities; when they turn **on** while armed, the **entry delay** starts, then the alarm triggers.
- **NFC Tag**: pick a tag from Tag Manager. If you prefer maximum convenience, enable **Allow any tag**.
- **Automatic disarm at**: time-of-day to disarm every morning (optional).

## Dashboard
Add a **Manual card** and paste the content from:  
`custom_components/ha_alarm_pro/dashboard/panel.yaml`

## Configuration & Options
Everything can be changed later in **Options** of the integration entry (volume, delays, mp3, NFC…).

## Known Limits
- This is intentionally **lightweight**. For advanced zones, partitions, or deep automation chains, consider more powerful alarm integrations.
- MP3 detection lists `.mp3` files under `/media` and `/config/www`. If nothing shows, verify your file locations and permissions.

## Support
Open issues/PRs in the repository. Contributions welcome!

## License
MIT
