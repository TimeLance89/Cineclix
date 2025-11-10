# NFC Alarm System - Projektstruktur

## Übersicht

Dieses Projekt ist eine vollständige HACS-Integration für Home Assistant, die ein NFC-basiertes Alarmsystem implementiert.

## Verzeichnisstruktur

```
nfc_alarm_system/
├── custom_components/
│   └── nfc_alarm_system/
│       ├── __init__.py                 # Hauptinitialisierung der Integration
│       ├── alarm_control_panel.py      # Alarm Control Panel Entity (Hauptlogik)
│       ├── config_flow.py              # Konfigurationsflow (UI-Setup)
│       ├── const.py                    # Konstanten und Konfigurationsschlüssel
│       ├── manifest.json               # Integration Manifest (Metadaten)
│       ├── services.yaml               # Service-Definitionen
│       ├── strings.json                # UI-Texte (Englisch)
│       └── translations/
│           └── de.json                 # Deutsche Übersetzungen
├── README.md                           # Hauptdokumentation
├── INSTALLATION.md                     # Detaillierte Installationsanleitung
├── CHANGELOG.md                        # Versionshistorie
├── CONTRIBUTING.md                     # Beitragsrichtlinien
├── LICENSE                             # MIT Lizenz
├── hacs.json                           # HACS Konfiguration
└── .gitignore                          # Git Ignore-Datei
```

## Dateibeschreibungen

### Core-Dateien (custom_components/nfc_alarm_system/)

#### `__init__.py`
Initialisiert die Integration und registriert die Plattformen. Enthält:
- `async_setup_entry()`: Setup-Funktion für Config Entry
- `async_unload_entry()`: Cleanup-Funktion
- Event-Listener für NFC-Tag Scans

#### `alarm_control_panel.py` (Hauptdatei - ca. 470 Zeilen)
Implementiert die Alarm Control Panel Entity mit vollständiger Logik:
- **Klasse**: `NFCAlarmPanel`
- **Zustände**: disarmed, arming, armed_away, pending, triggered
- **Hauptfunktionen**:
  - `_handle_tag_scanned()`: Verarbeitet NFC-Tag Events
  - `_start_arming_sequence()`: Exit Delay und Scharfschaltung
  - `_cancel_arming()`: Abbruch der Armierung
  - `_arm_alarm()`: Alarm scharfschalten
  - `_disarm_sequence()`: Alarm unscharfschalten
  - `_handle_sensor_triggered()`: Verarbeitet Sensor-Auslösungen
  - `_trigger_alarm()`: Alarm auslösen
  - `_play_siren()`: Sirene abspielen
  - `_pulse_red_lights()`: Rote Licht-Pulsierung
  - `_blink_lights()`: Lichter blinken lassen
  - `_set_light_color()`: Lichtfarbe setzen
  - `_send_notification()`: Benachrichtigungen senden

#### `config_flow.py` (ca. 200 Zeilen)
Implementiert den mehrstufigen Konfigurationsflow:
- **Schritt 1 (user)**: Grundkonfiguration (Name, Lichter, Sensoren, Delays)
- **Schritt 2 (nfc_tags)**: NFC-Tag Konfiguration
- **Schritt 3 (media)**: Medien & Sirene
- **Schritt 4 (notifications)**: Benachrichtigungen & Automatisierung
- **Options Flow**: Nachträgliche Anpassung der Verzögerungszeiten

#### `const.py`
Definiert alle Konstanten:
- Konfigurationsschlüssel (CONF_*)
- Standardwerte (DEFAULT_*)
- Alarm-Zustände
- Farbcodes für Lichter

#### `manifest.json`
Integration Manifest mit Metadaten:
- Domain: `nfc_alarm_system`
- Version: 1.0.0
- Config Flow aktiviert
- Keine externen Dependencies

#### `strings.json` & `translations/de.json`
UI-Texte für den Konfigurationsflow in Englisch und Deutsch.

#### `services.yaml`
Service-Definitionen (nutzt Standard Alarm Control Panel Services).

### Dokumentation

#### `README.md`
Hauptdokumentation mit:
- Funktionsübersicht
- Installationsanleitung (kurz)
- Konfigurationsübersicht
- Verwendungsbeispiele
- Fehlerbehebung
- Beispiel-Automationen

#### `INSTALLATION.md`
Detaillierte Schritt-für-Schritt Installationsanleitung:
- Voraussetzungen
- Installation via HACS
- Manuelle Installation
- Vollständige Konfiguration aller 5 Schritte
- Erste Tests
- Problemlösung
- Erweiterte Konfiguration

#### `CHANGELOG.md`
Versionshistorie und geplante Features.

#### `CONTRIBUTING.md`
Richtlinien für Entwickler, die beitragen möchten.

### Weitere Dateien

#### `LICENSE`
MIT Lizenz für Open Source Distribution.

#### `hacs.json`
HACS-spezifische Konfiguration für die Integration in HACS.

#### `.gitignore`
Standard Python/Home Assistant Ignore-Patterns.

## Technische Details

### Verwendete Home Assistant Konzepte

1. **Config Entry**: Moderne Konfiguration via UI
2. **Config Flow**: Mehrstufiger Setup-Prozess
3. **Alarm Control Panel Platform**: Standard HA Alarm-Entity
4. **Event Listener**: Für `tag_scanned` Events
5. **State Listener**: Für Sensor-Zustandsänderungen
6. **Services**: Standard `alarm_arm_away` und `alarm_disarm`
7. **Async/Await**: Vollständig asynchrone Implementierung

### State Machine

```
DISARMED ──(NFC Tag)──> ARMING ──(Exit Delay)──> ARMED_AWAY
    ^                      |                          |
    |                      |                          |
    |                  (NFC Tag)                 (Sensor)
    |                      |                          |
    |                      v                          v
    └──────────────── DISARMED                    PENDING
                                                      |
                                                      |
                                                 (Entry Delay)
                                                      |
                                                      v
                                                  TRIGGERED
                                                      |
                                                      |
                                                  (NFC Tag)
                                                      |
                                                      v
                                                  DISARMED
```

### Farbcodes

- 🟢 Grün (RGB: 0, 255, 0): Unscharfgeschaltet
- 🟡 Gelb (RGB: 255, 255, 0): Exit Delay
- 🟠 Orange (RGB: 255, 165, 0): Abbruch / Entry Delay
- 🔵 Blau (RGB: 0, 0, 255): Scharfgeschaltet
- 🔴 Rot (RGB: 255, 0, 0): Alarm ausgelöst

## Installation

1. **Via HACS**: Repository hinzufügen und installieren
2. **Manuell**: `custom_components/nfc_alarm_system/` nach Home Assistant kopieren
3. Home Assistant neu starten
4. Integration über UI hinzufügen

## Konfiguration

Die Integration verwendet einen 5-stufigen Config Flow:
1. Grundkonfiguration
2. NFC-Tags
3. Medien & Sirene
4. Benachrichtigungen & Automatisierung
5. Abschluss

Alle Einstellungen werden im Config Entry gespeichert und können über die UI verwaltet werden.

## Erweiterungsmöglichkeiten

- Zusätzliche Alarm-Modi (Home, Night)
- Zonen-Unterstützung
- Kamera-Integration
- Statistiken und Historie
- Benutzerverwaltung
- Keypad-Unterstützung
- Geofencing

## Support

- GitHub Issues für Fehlerberichte
- Logs unter Einstellungen → System → Protokolle
- Community-Forum für Fragen
