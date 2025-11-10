# Dashboard YAML-Konfiguration

Diese Anleitung zeigt dir, wie du das NFC Alarm System Dashboard **ohne Custom Card** direkt mit YAML-Konfiguration einrichtest.

## Vorteile der YAML-Lösung

- ✅ **Keine Custom Card nötig** - funktioniert sofort
- ✅ **Keine Ressourcen-Registrierung** erforderlich
- ✅ **Kein Browser-Cache-Problem**
- ✅ **Standard Home Assistant Komponenten**
- ✅ **Einfach anzupassen**

## Verfügbare Dateien

Das Projekt enthält zwei YAML-Konfigurationen:

### 1. `dashboard_simple.yaml` (Empfohlen)
- Funktioniert **ohne zusätzliche Plugins**
- Verwendet nur Standard Home Assistant Karten
- Einfach zu verstehen und anzupassen
- **→ Diese Version verwenden!**

### 2. `dashboard_example.yaml` (Erweitert)
- Benötigt **card-mod** Plugin für Styling
- Farbige Buttons und Animationen
- Nur verwenden wenn card-mod bereits installiert ist

## Installation - Schritt für Schritt

### Schritt 1: Dashboard öffnen

1. Gehe zu deinem Dashboard in Home Assistant
2. Klicke oben rechts auf **Bearbeiten** (Stift-Icon)

### Schritt 2: Karte hinzufügen

1. Klicke auf **+ Karte hinzufügen**
2. Scrolle ganz nach unten
3. Klicke auf **Manuell** (oder direkt auf den YAML-Editor)

### Schritt 3: YAML-Code einfügen

1. Öffne die Datei `dashboard_simple.yaml` aus dem ZIP
2. **Kopiere den gesamten Inhalt**
3. **Füge ihn in den YAML-Editor** ein

### Schritt 4: Sensoren und Lichter anpassen

**Wichtig:** Du musst die Beispiel-Entity-IDs durch deine tatsächlichen ersetzen!

#### So findest du deine Entity-IDs:

1. Gehe zu **Entwicklerwerkzeuge** → **Zustände**
2. Suche nach `alarm_control_panel.nfc_alarmsystem`
3. Klicke darauf
4. Unter **Attribute** findest du:
   - `trigger_sensors`: Liste deiner Sensoren
   - `indicator_lights`: Liste deiner Lichter

#### Beispiel:

**Attribute zeigen:**
```json
{
  "trigger_sensors": [
    "binary_sensor.haustuer",
    "binary_sensor.fenster_wohnzimmer"
  ],
  "indicator_lights": [
    "light.flur_indikator",
    "light.wohnzimmer_indikator"
  ]
}
```

**Im YAML ersetzen:**
```yaml
# Sensoren & Licht
- type: entities
  title: Sensoren & Licht
  entities:
    # Deine Sensoren
    - entity: binary_sensor.haustuer
      name: Haustür
    - entity: binary_sensor.fenster_wohnzimmer
      name: Fenster Wohnzimmer
    
    - type: divider
    
    # Deine Lichter
    - entity: light.flur_indikator
      name: Flur-Indikator
    - entity: light.wohnzimmer_indikator
      name: Wohnzimmer-Indikator
```

**Und im Logbook:**
```yaml
# Logbook/Verlauf
- type: logbook
  title: Verlauf (letzte 6 Stunden)
  hours_to_show: 6
  entities:
    - alarm_control_panel.nfc_alarmsystem
    - binary_sensor.haustuer
    - binary_sensor.fenster_wohnzimmer
```

### Schritt 5: Speichern

1. Klicke auf **Speichern**
2. Klicke auf **Fertig** (oben rechts)

## Dashboard-Aufbau

Die YAML-Konfiguration erstellt folgende Struktur:

### 1. Alarm-Warnung (Conditional)
- Wird **nur angezeigt** wenn Alarm ausgelöst ist
- Rotes Banner mit Warnung
- Anleitung zum Quittieren

### 2. Status-Sektion
- **Alarm-Status** mit letzter Änderung
- **Austrittsverzögerung** (Exit Delay)
- **Eintrittsverzögerung** (Entry Delay)
- **Sirenen-Lautstärke**

### 3. Buttons (2 Reihen à 2 Buttons)

**Reihe 1:**
- 🛡️ **Scharf (sofort)** - Alarm scharfschalten
- ✅ **Unscharf** - Alarm deaktivieren

**Reihe 2:**
- 🔔 **Alarm testen** - Testalarm auslösen
- 🔕 **Alarm quittieren** - Alarm bestätigen

### 4. Sensoren & Licht
- Liste aller **Trigger-Sensoren** mit Status
- Divider (Trennlinie)
- Liste aller **Indikator-Lichter** mit Status

### 5. Logbook/Verlauf
- Letzte **6 Stunden** Ereignisse
- Alle Entities (Alarm + Sensoren)
- Chronologische Auflistung

## Anpassungen

### Verlaufs-Zeitraum ändern

```yaml
- type: logbook
  hours_to_show: 12  # Statt 6 Stunden → 12 Stunden
```

### Button-Icons ändern

```yaml
- type: button
  name: Scharf
  icon: mdi:lock  # Anderes Icon
```

Verfügbare Icons: https://pictogrammers.com/library/mdi/

### Button-Größe ändern

```yaml
- type: button
  icon_height: 60px  # Größer (Standard: 40px)
```

### Weitere Sensoren hinzufügen

```yaml
entities:
  - entity: binary_sensor.sensor1
    name: Sensor 1
  - entity: binary_sensor.sensor2
    name: Sensor 2
  - entity: binary_sensor.sensor3  # Neu
    name: Sensor 3                  # Neu
```

## Erweiterte Version mit card-mod

Falls du **card-mod** installiert hast, kannst du `dashboard_example.yaml` verwenden für:

- 🎨 **Farbige Buttons** (Blau, Grün, Orange, Lila)
- ✨ **Puls-Animation** bei Alarm-Warnung
- 🎭 **Custom Styling**

### card-mod installieren (optional)

1. Öffne **HACS**
2. Suche nach "card-mod"
3. Installiere es
4. Starte Home Assistant neu
5. Verwende dann `dashboard_example.yaml`

## Fehlerbehebung

### "Entity not found"

**Problem:** Eine Entity-ID existiert nicht

**Lösung:**
1. Überprüfe die Entity-ID unter Entwicklerwerkzeuge → Zustände
2. Korrigiere die Schreibweise
3. Entferne die Zeile wenn die Entity nicht benötigt wird

### Buttons funktionieren nicht

**Problem:** Service-Aufrufe schlagen fehl

**Lösung:**
1. Teste die Services unter Entwicklerwerkzeuge → Dienste
2. Service: `alarm_control_panel.alarm_arm_away`
3. Entity: `alarm_control_panel.nfc_alarmsystem`

### Logbook zeigt keine Einträge

**Problem:** Keine Historie vorhanden

**Lösung:**
- Warte bis Zustandsänderungen stattgefunden haben
- Erhöhe `hours_to_show` auf 24 oder mehr
- Überprüfe ob History-Integration aktiviert ist

### Alarm-Warnung wird nicht angezeigt

**Problem:** Conditional Card funktioniert nicht

**Lösung:**
- Überprüfe ob die Entity-ID korrekt ist
- Teste ob der Alarm tatsächlich im State "triggered" ist
- Verwende Entwicklerwerkzeuge → Zustände zur Überprüfung

## Beispiel-Dashboard (Komplett)

Hier ein vollständiges Beispiel mit allen Anpassungen:

```yaml
type: vertical-stack
cards:
  - type: conditional
    conditions:
      - entity: alarm_control_panel.nfc_alarmsystem
        state: triggered
    card:
      type: markdown
      content: |
        ## 🔴 ALARM AUSGELÖST
        Quittiere den Alarm mit **„Alarm quittieren"** oder per NFC-Unscharf.

  - type: entities
    title: Status
    show_header_toggle: false
    state_color: true
    entities:
      - entity: alarm_control_panel.nfc_alarmsystem
        name: Alarm-Status
        secondary_info: last-changed
      - type: attribute
        entity: alarm_control_panel.nfc_alarmsystem
        attribute: exit_delay
        name: Austrittsverzögerung
        suffix: s
      - type: attribute
        entity: alarm_control_panel.nfc_alarmsystem
        attribute: entry_delay
        name: Eintrittsverzögerung
        suffix: s

  - type: horizontal-stack
    cards:
      - type: button
        name: Scharf
        icon: mdi:shield-check
        tap_action:
          action: call-service
          service: alarm_control_panel.alarm_arm_away
          target:
            entity_id: alarm_control_panel.nfc_alarmsystem
      - type: button
        name: Unscharf
        icon: mdi:shield-off
        tap_action:
          action: call-service
          service: alarm_control_panel.alarm_disarm
          target:
            entity_id: alarm_control_panel.nfc_alarmsystem

  - type: horizontal-stack
    cards:
      - type: button
        name: Test
        icon: mdi:alarm-light
        tap_action:
          action: call-service
          service: alarm_control_panel.alarm_trigger
          target:
            entity_id: alarm_control_panel.nfc_alarmsystem
      - type: button
        name: Quittieren
        icon: mdi:bell-cancel
        tap_action:
          action: call-service
          service: alarm_control_panel.alarm_disarm
          target:
            entity_id: alarm_control_panel.nfc_alarmsystem

  - type: entities
    title: Sensoren & Licht
    entities:
      - binary_sensor.haustuer
      - binary_sensor.fenster_wohnzimmer
      - type: divider
      - light.flur_indikator

  - type: logbook
    hours_to_show: 6
    entities:
      - alarm_control_panel.nfc_alarmsystem
      - binary_sensor.haustuer
      - binary_sensor.fenster_wohnzimmer
```

## Tipps

1. **Kopiere die YAML-Dateien** aus dem ZIP in einen Text-Editor
2. **Passe die Entity-IDs an** bevor du sie einfügst
3. **Teste Schritt für Schritt** - füge erst eine Karte hinzu, dann die nächste
4. **Nutze den visuellen Editor** für weitere Anpassungen nach dem Einfügen
5. **Speichere regelmäßig** während der Bearbeitung

## Support

Bei Problemen:
1. Überprüfe die YAML-Syntax (Einrückungen!)
2. Teste die Entity-IDs unter Entwicklerwerkzeuge → Zustände
3. Schaue in die Home Assistant Logs
4. Erstelle ein Issue auf GitHub mit deiner Konfiguration
