# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [1.0.0] - 2025-11-10

### Hinzugefügt
- Initiales Release der NFC Alarm System Integration
- NFC-Tag basierte Scharf-/Unscharfschaltung
- Unterstützung für ein oder zwei separate NFC-Tags
- Konfigurierbare Austrittsverzögerung (Exit Delay)
- Konfigurierbare Eintrittsverzögerung (Entry Delay)
- Visuelle Indikatoren mit Farbcodes:
  - Grün: Erfolgreich unscharfgeschaltet
  - Gelb: Armierung gestartet
  - Orange: Armierung abgebrochen / Entry Delay
  - Blau: Erfolgreich scharfgeschaltet
  - Rot: Alarm ausgelöst (pulsierend)
- Optionale Sirenen-Unterstützung über Media Player
- Optionale Push-Benachrichtigungen
- Optionale automatische Unscharfschaltung zu bestimmter Uhrzeit
- Mehrere Indikator-Lichter gleichzeitig unterstützt
- Mehrere Auslöser-Sensoren gleichzeitig unterstützt
- Benutzerfreundlicher Config Flow mit 5 Schritten
- Deutsche Übersetzungen
- HACS Kompatibilität
- Umfassende Dokumentation (README, INSTALLATION)

### Technische Details
- Alarm Control Panel Entity
- Event-basierte NFC-Tag Erkennung
- Asynchrone Implementierung
- State Machine für Alarm-Zustände
- Automatische Tag-ID Normalisierung (case-insensitive, ohne Bindestriche)

### Bekannte Einschränkungen
- Nur RGB-fähige Lichter werden für Farbindikatoren unterstützt
- Media Player muss `media_player.play_media` Service unterstützen
- Benachrichtigungen erfordern konfigurierte Notify-Services

## [Unreleased]

### Geplant für zukünftige Versionen
- Unterstützung für verschiedene Alarm-Modi (Home, Away, Night)
- Zeitbasierte Automatisierungen (z.B. automatisches Scharfschalten)
- Zonen-Unterstützung (verschiedene Bereiche separat scharf schalten)
- Integration mit Kamera-Aufnahmen bei Alarm
- Alarm-Historie und Statistiken
- Benutzerverwaltung mit verschiedenen NFC-Tags pro Person
- SMS/Email Benachrichtigungen zusätzlich zu Push
- Integration mit externen Sicherheitsdiensten
- Unterstützung für Keypad-Eingabe als Alternative zu NFC
- Geofencing-Integration (automatisch scharf/unscharf basierend auf Standort)
