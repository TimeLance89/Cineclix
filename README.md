# HA Alarm Lite (v0.4.1)

**Custom Integration** für Home Assistant – leicht einrichtbares, robustes Alarmsystem.

## Neu in v0.4.1 (2025-11-09)
- **MIT-Lizenz** hinzugefügt
- **GitHub Actions** für **HACS-Validation** & **hassfest** (CI)
- README erweitert (HACS/Release-Anleitung)

## Highlights
- Lock-basierte **State-Machine** (keine Race-Conditions)
- **RestoreEntity** (zustandssicher bei Neustarts)
- **Health-Checks** + Service `ha_alarm_lite.health_check`
- **Diagnostics** (exportierbar)
- **Onboarding-Dashboard** mit Selbsttests
- NFC-Tag-Feld im Options-Flow wird mit **letztem Scan** vorbefüllt

## Installation (HACS – Custom Repository)
1. Dieses Repo **öffentlich** machen und URL merken.
2. In Home Assistant: **HACS → Integrationen → Custom repositories**  
   - URL: `https://github.com/<DEIN-USER>/ha-alarm-lite`  
   - Category: **Integration** → Add
3. In HACS nach **HA Alarm Lite** suchen → **Installieren** → **HA neu starten**.
4. **Integration hinzufügen** und Optionen setzen (Indicator-Light, Siren-Player, MP3, Sensoren, Tag, Delays).

## Struktur
```
hacs.json
LICENSE
README.md
.github/workflows/hacs.yml
custom_components/ha_alarm_lite/
  ├── manifest.json
  ├── __init__.py
  ├── const.py
  ├── alarm_control_panel.py
  ├── config_flow.py
  ├── diagnostics.py
  ├── services.yaml
  └── dashboard/
      └── alarm_dashboard.yaml
```

## Schnellstart
- MP3 nach `/config/www/...`, z. B. `www/growzelt/alarm_active.mp3`  
- In den Optionen als `media-source://media_source/local/growzelt/alarm_active.mp3` eintragen.
- Entry-Sensoren wählen (z. B. Tür/Vibration), NFC-Tag scannen → in Optionen übernehmen.

## Releases & Tags
- Version in `manifest.json` bumpen (z. B. `0.4.1`).
- **Git-Tag** `v0.4.1` setzen und veröffentlichen, damit HACS Updates anzeigt.