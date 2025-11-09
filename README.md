# HA Alarm Lite

HA Alarm Lite is a small Home Assistant integration that turns a few sensors and an NFC tag into a reliable alarm system.
It arms with an exit delay, blinks a light for feedback, plays a local MP3 on a media player when triggered, and disarms by NFC or service call.
It restores state on restart, ships a simple dashboard, and includes diagnostics and a health check.

## What it does
- Arm (with exit delay) / Entry delay / Trigger
- Disarm by NFC tag or service
- Light feedback (blink patterns)
- Play a local MP3 on any `media_player`
- Health check + diagnostics
- Ready-made dashboard

## Setup (step by step)
1. Install via HACS (custom repository) and restart Home Assistant.
2. Add the integration: **Settings → Devices & Services → Add Integration → HA Alarm Lite**.
3. Select:
   - **Indicator light** – lamp that blinks for feedback
   - **Siren / Media player** – where the MP3 is played
   - **MP3 file** – pick a local `.mp3` (file picker)
   - **Entry sensors** – door/vibration/motion binary sensors
   - **NFC tag** – choose from your registered tags
   - **Exit delay / Entry delay** – seconds
   - **Auto disarm time** – optional daily time to disarm
4. Open the included dashboard “Alarm” and run the self-tests: *Test Indicator*, *Test Siren*, *Arm (Exit Delay)*, *Disarm*, *Trigger*.

## Notes
- The MP3 picker accepts files from `/media` or `/config/www` and converts them automatically to `media-source://`.
- The NFC selector lists all tags known to Home Assistant.
