# NFC Alarm System für Home Assistant

Eine vollständige HACS-Integration für ein NFC-basiertes Alarmsystem in Home Assistant.

## Funktionen

### Kernfunktionen
- **NFC-Tag basierte Steuerung**: Scharfschalten und Unscharfschalten per NFC-Tag
- **Austrittsverzögerung (Exit Delay)**: Konfigurierbare Zeit zum Verlassen nach dem Scharfschalten
- **Eintrittsverzögerung (Entry Delay)**: Zeit zum Unscharfschalten nach Auslösung
- **Visuelle Indikatoren**: Farbcodierte Lichtsignale für verschiedene Zustände
- **Sirenen-Unterstützung**: Optional Sirene über Media Player abspielen
- **Benachrichtigungen**: Optional Push-Benachrichtigungen bei Zustandsänderungen
- **Automatische Unscharfschaltung**: Optional zu einer bestimmten Uhrzeit

### Farbcodes der Indikator-Lichter
- 🟢 **Grün**: Erfolgreich unscharfgeschaltet
- 🟡 **Gelb**: Armierung gestartet (Exit Delay läuft)
- 🟠 **Orange**: Armierung abgebrochen / Eintrittsverzögerung (Entry Delay)
- 🔵 **Blau**: Erfolgreich scharfgeschaltet
- 🔴 **Rot**: Alarm ausgelöst (pulsierend)

## Dashboard-Karte

Diese Integration enthält eine **benutzerdefinierte Dashboard-Karte** mit professionellem Design:

- 🎨 Modernes Overlay-Design mit Statusanzeigen
- 📊 Verlauf der letzten 10 Ereignisse
- 🎛️ Interaktive Buttons (Scharfschalten, Unscharfschalten, Test)
- 📱 Responsive Design für alle Geräte
- 🌙 Dark Mode Unterstützung

**Siehe [DASHBOARD_KARTE.md](DASHBOARD_KARTE.md) für die vollständige Anleitung zur Dashboard-Karte.**

## Installation

### Via HACS (empfohlen)

1. Öffnen Sie HACS in Home Assistant
2. Gehen Sie zu "Integrationen"
3. Klicken Sie auf die drei Punkte oben rechts
4. Wählen Sie "Benutzerdefinierte Repositories"
5. Fügen Sie die Repository-URL hinzu: `https://github.com/yourusername/nfc_alarm_system`
6. Kategorie: "Integration"
7. Klicken Sie auf "Hinzufügen"
8. Suchen Sie nach "NFC Alarm System" und installieren Sie es
9. Starten Sie Home Assistant neu

### Manuelle Installation

1. Laden Sie die neueste Version herunter
2. Entpacken Sie die ZIP-Datei
3. Kopieren Sie den Ordner `custom_components/nfc_alarm_system` in Ihr Home Assistant `custom_components` Verzeichnis
4. Starten Sie Home Assistant neu

## Konfiguration

### Schritt 1: Integration hinzufügen

1. Gehen Sie zu **Einstellungen** → **Geräte & Dienste**
2. Klicken Sie auf **+ Integration hinzufügen**
3. Suchen Sie nach "NFC Alarm System"
4. Folgen Sie dem Konfigurationsassistenten

### Schritt 2: Grundkonfiguration

- **Name**: Geben Sie Ihrem Alarmsystem einen Namen
- **Indikator-Lichter**: Wählen Sie ein oder mehrere Lichter für visuelle Rückmeldungen
- **Auslöser-Sensoren**: Wählen Sie Tür-/Fenstersensoren, die das Alarm auslösen sollen
- **Austrittsverzögerung**: Zeit in Sekunden (Standard: 120s)
- **Eintrittsverzögerung**: Zeit in Sekunden (Standard: 30s)

### Schritt 3: NFC-Tag Konfiguration

- **Ein Tag für beide**: Aktivieren Sie dies, wenn Sie denselben Tag für Scharf- und Unscharfschalten verwenden möchten
- **NFC-Tag ID zum Scharfschalten**: Geben Sie die Tag-ID ein (z.B. `c44df694-639e-4608-a98d-35156be653b7`)
- **NFC-Tag ID zum Unscharfschalten**: Nur erforderlich, wenn Sie separate Tags verwenden

**So finden Sie Ihre NFC-Tag ID:**
1. Scannen Sie den Tag in Home Assistant
2. Gehen Sie zu **Entwicklerwerkzeuge** → **Ereignisse**
3. Hören Sie auf das Event `tag_scanned`
4. Die `tag_id` wird im Event-Payload angezeigt

### Schritt 4: Medien & Sirene (Optional)

- **Sirene aktivieren**: Aktivieren Sie dies, wenn Sie eine Sirene abspielen möchten
- **Media Player**: Wählen Sie einen Media Player (z.B. Google Nest Hub, Sonos)
- **Sirenen-Datei**: Pfad zur Audiodatei (z.B. `media-source://media_source/local/siren.mp3`)

**Sirenen-Datei hochladen:**
1. Legen Sie die MP3-Datei in `/config/www/` oder `/media/`
2. Verwenden Sie den Pfad: `media-source://media_source/local/dateiname.mp3`

### Schritt 5: Benachrichtigungen & Automatisierung (Optional)

- **Benachrichtigungen aktivieren**: Aktivieren für Push-Benachrichtigungen
- **Benachrichtigungs-Service**: z.B. `notify.mobile_app_iphone_von_max`
- **Automatische Unscharfschaltung**: Aktivieren für tägliche automatische Unscharfschaltung
- **Zeit**: Uhrzeit im Format HH:MM:SS (z.B. `06:00:00`)

## Verwendung

### Alarm scharfschalten

1. Scannen Sie Ihren NFC-Tag
2. Die Indikator-Lichter blinken **gelb** (2x)
3. Sie haben die konfigurierte Exit Delay Zeit, um das Gebäude zu verlassen
4. Bei erneutem Scannen während der Exit Delay wird die Armierung abgebrochen (orange)
5. Nach Ablauf der Zeit blinken die Lichter **blau** (2x) - Alarm ist scharf

### Alarm unscharfschalten

1. Scannen Sie Ihren NFC-Tag
2. Die Indikator-Lichter leuchten **grün** (1s)
3. Alarm ist unscharfgeschaltet

### Bei Auslösung

1. Sensor wird ausgelöst (z.B. Tür öffnet sich)
2. Indikator-Lichter leuchten **orange** (Entry Delay)
3. Sie haben die konfigurierte Entry Delay Zeit, um den NFC-Tag zu scannen
4. Wenn kein Tag gescannt wird:
   - Alarm wird ausgelöst
   - Lichter pulsieren **rot**
   - Sirene wird abgespielt (falls aktiviert)
   - Benachrichtigung wird gesendet (falls aktiviert)

## Fehlerbehebung

### NFC-Tag wird nicht erkannt

- Überprüfen Sie, ob die Tag-ID korrekt eingegeben wurde
- Tag-IDs sind case-insensitive und Bindestriche werden automatisch entfernt
- Testen Sie das Scannen über **Entwicklerwerkzeuge** → **Ereignisse** → `tag_scanned`

### Lichter reagieren nicht

- Stellen Sie sicher, dass die ausgewählten Lichter RGB-Farben unterstützen
- Überprüfen Sie, ob die Lichter erreichbar sind
- Prüfen Sie die Logs unter **Einstellungen** → **System** → **Protokolle**

### Sirene spielt nicht ab

- Überprüfen Sie den Dateipfad zur Sirenen-Datei
- Stellen Sie sicher, dass der Media Player verfügbar ist
- Testen Sie den Media Player manuell in Home Assistant

### Benachrichtigungen kommen nicht an

- Überprüfen Sie den Benachrichtigungs-Service Namen
- Format: `notify.mobile_app_gerätename`
- Testen Sie den Service über **Entwicklerwerkzeuge** → **Dienste**

## Technische Details

### Alarm-Zustände

- `disarmed`: Alarm ist unscharfgeschaltet
- `arming`: Exit Delay läuft
- `armed_away`: Alarm ist scharfgeschaltet
- `pending`: Entry Delay läuft (Sensor wurde ausgelöst)
- `triggered`: Alarm wurde ausgelöst

### Events

Die Integration hört auf folgende Events:
- `tag_scanned`: NFC-Tag wurde gescannt
- `state_changed`: Zustandsänderungen der Auslöser-Sensoren

### Services

Die Integration erstellt eine Alarm Control Panel Entity, die folgende Services unterstützt:
- `alarm_control_panel.alarm_arm_away`: Alarm scharfschalten
- `alarm_control_panel.alarm_disarm`: Alarm unscharfschalten

## Beispiel-Automationen

### Dashboard-Karte

```yaml
type: alarm-panel
entity: alarm_control_panel.nfc_alarmsystem
states:
  - arm_away
```

### Manuelle Steuerung per Automation

```yaml
# Alarm scharfschalten um 22:00
automation:
  - alias: "Alarm automatisch scharfschalten"
    trigger:
      - platform: time
        at: "22:00:00"
    action:
      - service: alarm_control_panel.alarm_arm_away
        target:
          entity_id: alarm_control_panel.nfc_alarmsystem
```

## Changelog

### Version 1.0.0
- Initiales Release
- NFC-Tag basierte Steuerung
- Konfigurierbare Exit/Entry Delays
- Visuelle Indikatoren
- Sirenen-Unterstützung
- Benachrichtigungen
- Automatische Unscharfschaltung

## Support

Bei Fragen oder Problemen:
- Erstellen Sie ein Issue auf GitHub
- Überprüfen Sie die Logs in Home Assistant
- Stellen Sie sicher, dass Sie die neueste Version verwenden

## Lizenz

MIT License - siehe LICENSE Datei

## Credits

Entwickelt für die Home Assistant Community.
Basierend auf den Anforderungen eines benutzerdefinierten Alarmsystems mit NFC-Integration.
