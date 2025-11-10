# Installationsanleitung - NFC Alarm System

Diese Anleitung führt Sie Schritt für Schritt durch die Installation und Einrichtung des NFC Alarm Systems für Home Assistant.

## Voraussetzungen

- Home Assistant Core 2023.1.0 oder höher
- HACS (Home Assistant Community Store) installiert (empfohlen)
- Mindestens ein NFC-Tag
- Mindestens ein RGB-fähiges Licht (für Indikator)
- Mindestens ein Tür-/Fenstersensor

## Installation

### Methode 1: Installation via HACS (Empfohlen)

#### Schritt 1: Repository zu HACS hinzufügen

1. Öffnen Sie Home Assistant
2. Navigieren Sie zu **HACS** im Seitenmenü
3. Klicken Sie auf **Integrationen**
4. Klicken Sie auf die **drei Punkte** (⋮) oben rechts
5. Wählen Sie **Benutzerdefinierte Repositories**
6. Geben Sie die Repository-URL ein: `https://github.com/yourusername/nfc_alarm_system`
7. Wählen Sie als Kategorie: **Integration**
8. Klicken Sie auf **Hinzufügen**

#### Schritt 2: Integration installieren

1. Suchen Sie in HACS nach "NFC Alarm System"
2. Klicken Sie auf die Integration
3. Klicken Sie auf **Herunterladen**
4. Wählen Sie die neueste Version
5. Klicken Sie auf **Herunterladen**

#### Schritt 3: Home Assistant neu starten

1. Gehen Sie zu **Einstellungen** → **System**
2. Klicken Sie auf **Neu starten**
3. Bestätigen Sie den Neustart

### Methode 2: Manuelle Installation

#### Schritt 1: Dateien herunterladen

1. Laden Sie die neueste Version als ZIP-Datei herunter
2. Entpacken Sie die ZIP-Datei

#### Schritt 2: Dateien kopieren

1. Verbinden Sie sich mit Ihrem Home Assistant System (z.B. via Samba, SSH)
2. Navigieren Sie zum `config` Verzeichnis
3. Erstellen Sie den Ordner `custom_components`, falls er nicht existiert
4. Kopieren Sie den Ordner `nfc_alarm_system` nach `config/custom_components/`

Die Struktur sollte so aussehen:
```
config/
└── custom_components/
    └── nfc_alarm_system/
        ├── __init__.py
        ├── alarm_control_panel.py
        ├── config_flow.py
        ├── const.py
        ├── manifest.json
        ├── strings.json
        └── translations/
            └── de.json
```

#### Schritt 3: Home Assistant neu starten

1. Gehen Sie zu **Einstellungen** → **System**
2. Klicken Sie auf **Neu starten**
3. Bestätigen Sie den Neustart

## Konfiguration

### Schritt 1: Integration hinzufügen

1. Warten Sie, bis Home Assistant vollständig neu gestartet ist
2. Gehen Sie zu **Einstellungen** → **Geräte & Dienste**
3. Klicken Sie auf **+ Integration hinzufügen** (unten rechts)
4. Suchen Sie nach "NFC Alarm System"
5. Klicken Sie auf die Integration

### Schritt 2: Grundkonfiguration ausfüllen

#### Name des Alarmsystems
- Geben Sie einen Namen ein (z.B. "Hausalarm", "Büro Alarm")
- Dieser Name wird für die Entity verwendet

#### Indikator-Lichter auswählen
- Klicken Sie in das Feld
- Wählen Sie ein oder mehrere RGB-fähige Lichter aus
- Diese Lichter zeigen den Status des Alarms durch Farben an
- **Empfehlung**: Verwenden Sie Hue, LIFX oder andere RGB-Lampen

#### Auslöser-Sensoren auswählen
- Klicken Sie in das Feld
- Wählen Sie alle Sensoren aus, die den Alarm auslösen sollen
- Typischerweise: Tür-/Fenstersensoren, Bewegungsmelder
- **Wichtig**: Nur Binary Sensors mit `device_class: door`, `window` oder `motion`

#### Verzögerungszeiten einstellen
- **Austrittsverzögerung (Exit Delay)**: Zeit in Sekunden, die Sie haben, um das Gebäude zu verlassen, nachdem Sie den Alarm scharfgeschaltet haben
  - Standard: 120 Sekunden (2 Minuten)
  - Empfehlung: 60-180 Sekunden
  
- **Eintrittsverzögerung (Entry Delay)**: Zeit in Sekunden, die Sie haben, um den Alarm zu deaktivieren, nachdem ein Sensor ausgelöst wurde
  - Standard: 30 Sekunden
  - Empfehlung: 20-60 Sekunden

Klicken Sie auf **Weiter**

### Schritt 3: NFC-Tags konfigurieren

#### NFC-Tag ID herausfinden

**Wichtig**: Führen Sie dies aus, BEVOR Sie fortfahren!

1. Öffnen Sie **Entwicklerwerkzeuge** → **Ereignisse**
2. Geben Sie im Feld "Auf Ereignis lauschen" ein: `tag_scanned`
3. Klicken Sie auf **Lauschen starten**
4. Scannen Sie Ihren NFC-Tag mit Ihrem Smartphone/Tablet
5. Im Ereignis-Bereich erscheint ein neues Event
6. Kopieren Sie die `tag_id` (z.B. `c44df694-639e-4608-a98d-35156be653b7`)

#### Konfiguration

- **Ein Tag für beide**: 
  - ✅ Aktiviert: Derselbe Tag schaltet scharf UND unscharf (empfohlen für Anfänger)
  - ❌ Deaktiviert: Separate Tags für Scharf- und Unscharfschalten

- **NFC-Tag ID zum Scharfschalten**: 
  - Fügen Sie die kopierte Tag-ID ein
  - Format: `c44df694-639e-4608-a98d-35156be653b7`

- **NFC-Tag ID zum Unscharfschalten** (nur wenn "Ein Tag für beide" deaktiviert):
  - Fügen Sie die Tag-ID des zweiten Tags ein

Klicken Sie auf **Weiter**

### Schritt 4: Medien & Sirene (Optional)

Diese Einstellungen sind optional. Wenn Sie keine Sirene verwenden möchten, lassen Sie "Sirene aktivieren" deaktiviert.

#### Sirene aktivieren
- ✅ Aktiviert: Sirene wird bei Alarm abgespielt
- ❌ Deaktiviert: Keine Sirene (nur visuelle Indikatoren)

#### Media Player (nur wenn Sirene aktiviert)
- Wählen Sie einen Media Player aus
- Geeignet: Google Nest Hub, Sonos, Echo, etc.
- **Tipp**: Wählen Sie einen Player mit guter Lautstärke

#### Sirenen-Datei (nur wenn Sirene aktiviert)
- Pfad zur Sirenen-Audiodatei
- Format: `media-source://media_source/local/dateiname.mp3`

**So laden Sie eine Sirenen-Datei hoch:**
1. Laden Sie eine Sirenen-MP3-Datei herunter (z.B. von freesound.org)
2. Öffnen Sie **Medien** in Home Assistant
3. Klicken Sie auf **Hochladen**
4. Wählen Sie Ihre MP3-Datei
5. Notieren Sie den Dateinamen (z.B. `siren.mp3`)
6. Verwenden Sie: `media-source://media_source/local/siren.mp3`

Klicken Sie auf **Weiter**

### Schritt 5: Benachrichtigungen & Automatisierung

#### Benachrichtigungen aktivieren
- ✅ Aktiviert: Push-Benachrichtigungen bei Zustandsänderungen
- ❌ Deaktiviert: Keine Benachrichtigungen

#### Benachrichtigungs-Service (nur wenn aktiviert)
- Format: `notify.mobile_app_gerätename`
- Beispiel: `notify.mobile_app_iphone_von_max`

**So finden Sie Ihren Service-Namen:**
1. Gehen Sie zu **Entwicklerwerkzeuge** → **Dienste**
2. Suchen Sie nach "notify"
3. Wählen Sie Ihren Service aus der Liste
4. Der Name steht oben (z.B. `notify.mobile_app_pixel_7`)

#### Automatische Unscharfschaltung
- ✅ Aktiviert: Alarm wird täglich zu einer bestimmten Zeit automatisch unscharfgeschaltet
- ❌ Deaktiviert: Keine automatische Unscharfschaltung

#### Zeit für automatische Unscharfschaltung (nur wenn aktiviert)
- Wählen Sie die Uhrzeit (z.B. 06:00:00 für 6 Uhr morgens)
- Format: HH:MM:SS

Klicken Sie auf **Absenden**

## Erste Schritte

### 1. Dashboard-Karte hinzufügen

1. Gehen Sie zu Ihrem Dashboard
2. Klicken Sie auf **Bearbeiten**
3. Klicken Sie auf **+ Karte hinzufügen**
4. Suchen Sie nach "Alarm Panel"
5. Wählen Sie Ihre Alarm-Entity aus
6. Klicken Sie auf **Speichern**

Beispiel YAML:
```yaml
type: alarm-panel
entity: alarm_control_panel.nfc_alarmsystem
states:
  - arm_away
```

### 2. Ersten Test durchführen

#### Test 1: Scharfschalten
1. Scannen Sie Ihren NFC-Tag
2. Die Indikator-Lichter sollten **gelb** blinken (2x)
3. Warten Sie die Exit Delay ab
4. Die Lichter sollten **blau** blinken (2x)
5. Status im Dashboard sollte "Scharf" anzeigen

#### Test 2: Unscharfschalten
1. Scannen Sie Ihren NFC-Tag erneut
2. Die Indikator-Lichter sollten **grün** leuchten (1s)
3. Status im Dashboard sollte "Unscharf" anzeigen

#### Test 3: Alarm auslösen
1. Schalten Sie den Alarm scharf (siehe Test 1)
2. Öffnen Sie eine Tür/Fenster mit konfiguriertem Sensor
3. Die Lichter sollten **orange** leuchten (Entry Delay)
4. Warten Sie die Entry Delay ab OHNE Tag zu scannen
5. Die Lichter sollten **rot** pulsieren
6. Sirene sollte abspielen (falls konfiguriert)
7. Benachrichtigung sollte ankommen (falls konfiguriert)

#### Test 4: Alarm während Entry Delay deaktivieren
1. Schalten Sie den Alarm scharf
2. Öffnen Sie eine Tür/Fenster
3. Scannen Sie den NFC-Tag INNERHALB der Entry Delay
4. Alarm sollte deaktiviert werden (grün)

## Problemlösung

### Integration erscheint nicht in der Liste

**Lösung:**
1. Überprüfen Sie, ob die Dateien korrekt kopiert wurden
2. Prüfen Sie die Logs: **Einstellungen** → **System** → **Protokolle**
3. Suchen Sie nach Fehlern mit "nfc_alarm_system"
4. Starten Sie Home Assistant erneut

### NFC-Tag wird nicht erkannt

**Lösung:**
1. Überprüfen Sie die Tag-ID in der Konfiguration
2. Scannen Sie den Tag und prüfen Sie das `tag_scanned` Event
3. Vergleichen Sie die IDs (Groß-/Kleinschreibung wird ignoriert)
4. Bindestriche werden automatisch entfernt

### Lichter reagieren nicht

**Lösung:**
1. Testen Sie die Lichter manuell in Home Assistant
2. Stellen Sie sicher, dass sie RGB-Farben unterstützen
3. Prüfen Sie die Entity-IDs in der Konfiguration
4. Schauen Sie in die Logs nach Fehlermeldungen

### Sirene spielt nicht ab

**Lösung:**
1. Testen Sie den Media Player manuell
2. Überprüfen Sie den Dateipfad zur Sirene
3. Stellen Sie sicher, dass die Datei existiert
4. Prüfen Sie, ob der Media Player verfügbar ist

### Benachrichtigungen kommen nicht an

**Lösung:**
1. Testen Sie den Notify-Service manuell über Entwicklerwerkzeuge
2. Überprüfen Sie den Service-Namen (Format: `notify.mobile_app_xxx`)
3. Stellen Sie sicher, dass die Home Assistant App auf dem Smartphone installiert ist
4. Prüfen Sie die Benachrichtigungseinstellungen auf dem Smartphone

## Erweiterte Konfiguration

### Optionen ändern

1. Gehen Sie zu **Einstellungen** → **Geräte & Dienste**
2. Suchen Sie "NFC Alarm System"
3. Klicken Sie auf **Konfigurieren**
4. Ändern Sie die Verzögerungszeiten
5. Klicken Sie auf **Absenden**

### Integration neu konfigurieren

1. Gehen Sie zu **Einstellungen** → **Geräte & Dienste**
2. Suchen Sie "NFC Alarm System"
3. Klicken Sie auf die **drei Punkte** (⋮)
4. Wählen Sie **Löschen**
5. Fügen Sie die Integration erneut hinzu (siehe oben)

## Nächste Schritte

- Erstellen Sie Automationen für zusätzliche Funktionen
- Integrieren Sie das Alarm System in Ihre Szenen
- Fügen Sie weitere Sensoren hinzu
- Passen Sie die Verzögerungszeiten an Ihre Bedürfnisse an

## Support

Bei Problemen:
1. Überprüfen Sie die Logs
2. Lesen Sie die README.md
3. Erstellen Sie ein Issue auf GitHub mit:
   - Home Assistant Version
   - Fehlermeldung aus den Logs
   - Beschreibung des Problems
   - Schritte zur Reproduktion
