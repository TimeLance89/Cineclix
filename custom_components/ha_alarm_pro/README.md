# HA Alarm Pro (v0.4.0)

## English

### Highlights
- Single `alarm_control_panel` entity with entry/exit delays and indicator light feedback.
- NFC tag workflow redesigned: authorized tags can arm (with selectable default mode) or disarm the alarm, including during pending/triggered states.
- Optional siren playback through a media player with curated audio suggestions from Home Assistant's `/media` and `/config/www` folders (manual paths are also supported for advanced setups).
- Intelligent audio cues: define dedicated entry/exit chimes with adaptive countdown pacing and their own volume level so occupants instantly know how much time is left.
- Automatic disarm scheduling and optional acceptance of any tag (or any tag while triggered).
- Lovelace dashboard snippet available in `dashboard/panel.yaml`.

### Tag arming logic
1. Scan an authorized tag while disarmed to arm the system in the configured mode (Home or Away). Exit delay is applied automatically.
2. Scan the same tag while armed, pending, or arming to disarm immediately.
3. When triggered, authorized tags (and, if enabled, any tag) will disarm and stop the siren.

### Installation
1. Copy `custom_components/ha_alarm_pro/` to `/config/custom_components/` (or install via HACS as a custom repository).
2. Restart Home Assistant.
3. Add the integration via **Settings → Devices & Services → Add Integration → HA Alarm Pro**.
4. During setup, pick devices, MP3, tags, and timers. All settings remain editable via the Options flow.

### Dashboard
Add a Manual card and paste the YAML from `custom_components/ha_alarm_pro/dashboard/panel.yaml` to replicate the reference UI. The example shows a triggered alarm banner, quick-action buttons (arm home/away, disarm, trigger), key attributes such as entry delay state or last NFC tag, plus a logbook and placeholders for your entry sensors and indicator light. Replace the placeholder entity IDs (`binary_sensor.tuer_vorne`, `light.flur_alarmindikator`, …) with the devices from your setup.

---

## Deutsch

### Highlights
- Eine einzelne `alarm_control_panel`-Entität mit Ein-/Austrittsverzögerung und optionaler Signalleuchte.
- Neu aufgebauter NFC-Ablauf: Autorisierte Tags schalten die Anlage scharf (mit wählbarem Standardmodus) oder entschärfen sie – auch während Pending- und Alarmzuständen.
- Optionale Sirene über einen Medienplayer; alle vorhandenen Audiodateien aus `/media` und `/config/www` werden automatisch vorgeschlagen – bei Bedarf kann dennoch ein eigener Pfad hinterlegt werden.
- Clevere akustische Hinweise: Separate Signaltöne für Ein- und Austrittsverzögerung mit dynamischer Taktung und eigener Lautstärke machen den Restlauf der Verzögerung hörbar.
- Zeitgesteuerte Entschärfung sowie optionales Zulassen beliebiger Tags (auch nur im Alarmfall).
- Lovelace-Dashboard-Snippet in `dashboard/panel.yaml` enthalten.

### Tag-Logik
1. Autorisiertes Tag im entschärften Zustand scannen → Anlage wird mit der gewählten Voreinstellung (Zuhause oder Abwesend) samt Auslöseverzögerung scharf geschaltet.
2. Dasselbe Tag während scharfem, Pending- oder Scharf-Schalten-Zustand scannen → sofortige Entschärfung.
3. Im ausgelösten Zustand entschärfen autorisierte Tags (und – falls aktiviert – beliebige Tags) und stoppen die Sirene.

### Installation
1. `custom_components/ha_alarm_pro/` nach `/config/custom_components/` kopieren (oder als HACS-Custom-Repository installieren).
2. Home Assistant neu starten.
3. Integration über **Einstellungen → Geräte & Dienste → Integration hinzufügen → HA Alarm Pro** einrichten.
4. Während der Einrichtung Geräte, MP3-Datei, Tags und Zeitparameter wählen; alle Einstellungen lassen sich später im Optionsdialog ändern.

### Dashboard
Füge eine manuelle Karte hinzu und kopiere den YAML-Code aus `custom_components/ha_alarm_pro/dashboard/panel.yaml`, um die Beispieloberfläche zu übernehmen. Das Beispiel enthält einen Alarm-Hinweis, Schnellbedienungstasten (Zuhause/Abwesend scharf, Unscharf, Testalarm), wichtige Attribute wie die Eintrittsverzögerung oder den letzten NFC-Tag sowie ein Logbuch. Ersetze die Platzhalter-Entitäten (`binary_sensor.tuer_vorne`, `light.flur_alarmindikator`, …) durch die Geräte deiner Installation.
