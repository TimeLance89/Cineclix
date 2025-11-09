# HA Alarm Pro - Dashboard Integration

## Automatisches Dashboard

Diese Integration stellt eine fertige Dashboard-Konfiguration bereit, die alle Funktionen der Alarmanlage zugänglich macht.

## Dashboard-Funktionen

### Statusanzeige
- Aktueller Alarmzustand (Scharf/Unscharf/Ausgelöst)
- Eintrittsverzögerung aktiv/inaktiv
- Restzeit der Eintrittsverzögerung
- Letzter ausgelöster Sensor
- Letzter verwendeter NFC-Tag
- Letzte Tag-Aktion

### Steuerungsbuttons

**Reihe 1:**
- **Scharf (Abwesend)** - Aktiviert den Alarm im Away-Modus
- **Scharf (Zuhause)** - Aktiviert den Alarm im Home-Modus

**Reihe 2:**
- **Unscharf** - Deaktiviert den Alarm
- **Alarm testen** - Löst einen Test-Alarm aus
- **Alarm quittieren** - Deaktiviert einen ausgelösten Alarm
- **Sound testen** - Spielt den Alarmton zur Überprüfung ab

### Sensoren & Indikatoren
Zeigt alle konfigurierten Eingangssensoren und Indikator-Lichter an.

### Alarm-Historie
Logbook mit den letzten 6 Stunden Aktivität.

## Installation des Dashboards

### Methode 1: Manuelles Hinzufügen (Empfohlen)

1. Öffnen Sie Ihr Home Assistant Dashboard
2. Klicken Sie auf die drei Punkte (⋮) oben rechts
3. Wählen Sie **„Dashboard bearbeiten"**
4. Klicken Sie auf **„+ Karte hinzufügen"**
5. Scrollen Sie nach unten und wählen Sie **„Manuell"**
6. Kopieren Sie den Inhalt der Datei `panel.yaml` aus diesem Ordner
7. Passen Sie die Platzhalter-Entitäten an Ihre tatsächlichen Sensoren und Lichter an:
   - Ersetzen Sie `binary_sensor.example_door_sensor` mit Ihren Sensoren
   - Ersetzen Sie `light.example_indicator` mit Ihren Lichtern
8. Klicken Sie auf **„Speichern"**

### Methode 2: Als separates Dashboard

1. Gehen Sie zu **Einstellungen** → **Dashboards**
2. Klicken Sie auf **„+ Dashboard hinzufügen"**
3. Wählen Sie **„Neues Dashboard"**
4. Name: "Alarm Pro"
5. Icon: `mdi:shield-home`
6. Wählen Sie **„Nur YAML"** als Modus
7. Fügen Sie den Inhalt der `panel.yaml` ein
8. Passen Sie die Entitäten an

## Anpassung

### Sensoren anpassen

Ersetzen Sie im Abschnitt "Sensoren & Indikatoren":

```yaml
entities:
  - entity: binary_sensor.aqara_vibration_sensor_t1_belegung
    name: Tür/Vibration 1
  - entity: binary_sensor.aqara_vibration_sensor_t1_belegung_2
    name: Tür/Vibration 2
  - type: divider
  - entity: light.hue_color_lamp_3
    name: Flur-Indikator
```

### Logbook anpassen

Fügen Sie im Logbook-Abschnitt Ihre Entitäten hinzu:

```yaml
entities:
  - alarm_control_panel.ha_alarm_pro
  - binary_sensor.aqara_vibration_sensor_t1_belegung
  - binary_sensor.aqara_vibration_sensor_t1_belegung_2
  - light.hue_color_lamp_3
```

## Beispiel-Dashboard

Ein vollständig konfiguriertes Beispiel basierend auf Ihren Automationen:

```yaml
type: vertical-stack
cards:
  - type: conditional
    conditions:
      - entity: alarm_control_panel.ha_alarm_pro
        state: triggered
    card:
      type: markdown
      content: |
        ## 🔴 ALARM AUSGELÖST
        Quittiere den Alarm mit **„Alarm quittieren"** oder per NFC-Tag.

  - type: entities
    title: Alarm-Status
    show_header_toggle: false
    state_color: true
    entities:
      - entity: alarm_control_panel.ha_alarm_pro
        name: Alarmanlage

  - type: horizontal-stack
    cards:
      - type: button
        name: Scharf (Abwesend)
        icon: mdi:shield-lock
        tap_action:
          action: call-service
          service: alarm_control_panel.alarm_arm_away
          target:
            entity_id: alarm_control_panel.ha_alarm_pro
      - type: button
        name: Scharf (Zuhause)
        icon: mdi:shield-home
        tap_action:
          action: call-service
          service: alarm_control_panel.alarm_arm_home
          target:
            entity_id: alarm_control_panel.ha_alarm_pro

  - type: horizontal-stack
    cards:
      - type: button
        name: Unscharf
        icon: mdi:shield-off
        tap_action:
          action: call-service
          service: alarm_control_panel.alarm_disarm
          target:
            entity_id: alarm_control_panel.ha_alarm_pro
      - type: button
        name: Alarm testen
        icon: mdi:alarm-light
        tap_action:
          action: call-service
          service: ha_alarm_pro.test_alarm
          target:
            entity_id: alarm_control_panel.ha_alarm_pro
      - type: button
        name: Alarm quittieren
        icon: mdi:bell-cancel
        tap_action:
          action: call-service
          service: alarm_control_panel.alarm_disarm
          target:
            entity_id: alarm_control_panel.ha_alarm_pro
      - type: button
        name: Sound testen
        icon: mdi:volume-high
        tap_action:
          action: call-service
          service: ha_alarm_pro.test_alarm_sound
          target:
            entity_id: alarm_control_panel.ha_alarm_pro

  - type: entities
    title: Sensoren & Indikatoren
    show_header_toggle: false
    state_color: true
    entities:
      - entity: binary_sensor.aqara_vibration_sensor_t1_belegung
        name: Tür/Vibration 1
      - entity: binary_sensor.aqara_vibration_sensor_t1_belegung_2
        name: Tür/Vibration 2
      - type: divider
      - entity: light.hue_color_lamp_3
        name: Flur-Indikator

  - type: logbook
    title: Alarm-Historie (6 Stunden)
    hours_to_show: 6
    entities:
      - alarm_control_panel.ha_alarm_pro
      - binary_sensor.aqara_vibration_sensor_t1_belegung
      - binary_sensor.aqara_vibration_sensor_t1_belegung_2
```

## Hinweise

- Das Dashboard verwendet die Standard-Lovelace-Karten von Home Assistant
- Alle Buttons sind sofort funktionsfähig nach der Installation
- Die Statusanzeigen aktualisieren sich automatisch
- Das Logbook zeigt die Historie aller relevanten Ereignisse

## Troubleshooting

**Problem:** Buttons funktionieren nicht
- **Lösung:** Überprüfen Sie, ob die Integration korrekt installiert ist
- Überprüfen Sie, ob die Entity `alarm_control_panel.ha_alarm_pro` existiert

**Problem:** Sensoren werden nicht angezeigt
- **Lösung:** Passen Sie die Entity-IDs im Dashboard an Ihre tatsächlichen Sensoren an

**Problem:** Conditional Card wird nicht angezeigt
- **Lösung:** Dies ist normal - die Karte erscheint nur, wenn der Alarm ausgelöst ist
