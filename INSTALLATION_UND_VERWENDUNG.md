# HA Alarm Pro - Installation und Verwendung (Version 0.5.0)

## Übersicht der neuen Funktionen

Diese aktualisierte Version der HA Alarm Pro Integration behebt drei wesentliche Probleme und erweitert die Funktionalität erheblich. Die Integration bietet nun einen Test-Service für Alarmtöne, erweiterte Unterstützung für verschiedene Audiodateiformate mit automatischer Erkennung aller verfügbaren Dateien sowie die Möglichkeit, mehrere Lichtquellen gleichzeitig als Alarm-Indikatoren zu verwenden.

## Installation

Die Installation erfolgt durch Kopieren des aktualisierten `custom_components/ha_alarm_pro` Ordners in Ihr Home Assistant Konfigurationsverzeichnis. Nach dem Kopieren muss Home Assistant neu gestartet werden, damit die Änderungen wirksam werden.

### Schritt-für-Schritt Anleitung

Navigieren Sie zu Ihrem Home Assistant Konfigurationsverzeichnis (üblicherweise `/config/`). Falls der Ordner `custom_components` noch nicht existiert, erstellen Sie diesen. Kopieren Sie den gesamten `ha_alarm_pro` Ordner in das `custom_components` Verzeichnis. Die finale Struktur sollte `/config/custom_components/ha_alarm_pro/` sein.

Starten Sie Home Assistant neu, entweder über die Benutzeroberfläche unter Einstellungen → System → Neu starten oder über die Kommandozeile mit dem entsprechenden Befehl für Ihre Installation.

## Konfiguration

### Mehrere Lichtquellen hinzufügen

Die Integration unterstützt nun die Auswahl mehrerer Lichtquellen, die synchron gesteuert werden. Öffnen Sie dazu die Einstellungen und navigieren Sie zu Geräte & Dienste. Suchen Sie die HA Alarm Pro Integration und klicken Sie auf Konfigurieren. Im Feld "Indicator Light" können Sie nun mehrere Lichtquellen auswählen, indem Sie auf das Dropdown-Menü klicken und mehrere Entitäten markieren.

Alle ausgewählten Lichter werden gleichzeitig gesteuert und zeigen denselben Status an. Beim Scharfschalten blinken sie gelb, während der Eintrittsverzögerung blinken sie orange, und im Alarmzustand blinken sie rot.

### Audiodateien hinzufügen

Die Integration erkennt automatisch alle Audiodateien in den Verzeichnissen `/media/` und `/www/`. Unterstützt werden die Formate MP3, WAV, OGG, FLAC, M4A und AAC.

Um neue Audiodateien hinzuzufügen, öffnen Sie einen Dateimanager wie den File Editor Add-on. Navigieren Sie zum Ordner `/media/` oder `/config/www/`. Erstellen Sie optional einen Unterordner wie `/media/alarm_sounds/` für eine bessere Organisation. Laden Sie Ihre Audiodateien in diesen Ordner hoch.

Nach dem Hochladen öffnen Sie die Konfiguration der HA Alarm Pro Integration erneut. Die neuen Dateien erscheinen automatisch in den Dropdown-Menüs für Alarmton, Exit-Delay-Sound und Entry-Delay-Sound. Die Dateien werden mit ihrem Namen und dem vollständigen Pfad angezeigt.

Sie können auch benutzerdefinierte Pfade manuell eingeben, wenn die Dateien an einem anderen Ort gespeichert sind. Für Media-Source URLs verwenden Sie das Format `media-source://media_source/local/dateiname.mp3`.

## Verwendung des Test-Services

Der neue Service `ha_alarm_pro.test_alarm_sound` ermöglicht es Ihnen, den konfigurierten Alarmton zu testen, ohne den Alarm tatsächlich auszulösen. Dies ist besonders nützlich, um die Lautstärke und den Sound zu überprüfen.

### Manueller Test über die Entwicklerwerkzeuge

Öffnen Sie die Entwicklerwerkzeuge in Home Assistant unter Entwicklerwerkzeuge → Dienste. Wählen Sie den Service `ha_alarm_pro.test_alarm_sound` aus. Geben Sie die Entity-ID Ihrer Alarmanlage ein, typischerweise `alarm_control_panel.ha_alarm_pro`. Klicken Sie auf "Dienst aufrufen", um den Alarmton abzuspielen.

### Verwendung in Automationen

Sie können den Test-Service auch in Automationen integrieren. Ein Beispiel für eine Automation, die den Alarmton bei Betätigung eines Buttons testet:

```yaml
automation:
  - alias: "Alarmton testen"
    trigger:
      - platform: state
        entity_id: input_button.test_alarm_sound
        to: "on"
    action:
      - service: ha_alarm_pro.test_alarm_sound
        data:
          entity_id: alarm_control_panel.ha_alarm_pro
```

### Verwendung in Scripts

Der Service kann auch in Scripts verwendet werden, um verschiedene Sounds zu testen oder komplexere Testszenarien zu erstellen:

```yaml
script:
  test_alarm_system:
    sequence:
      - service: ha_alarm_pro.test_alarm_sound
        data:
          entity_id: alarm_control_panel.ha_alarm_pro
      - delay:
          seconds: 5
      - service: notify.mobile_app
        data:
          message: "Alarmton-Test abgeschlossen"
```

## Fehlerbehebung

### Audiodateien werden nicht angezeigt

Wenn Ihre hochgeladenen Audiodateien nicht in der Auswahlliste erscheinen, überprüfen Sie zunächst, ob die Dateien tatsächlich in den Verzeichnissen `/media/` oder `/config/www/` gespeichert sind. Stellen Sie sicher, dass die Dateierweiterung zu den unterstützten Formaten gehört (mp3, wav, ogg, flac, m4a, aac). Öffnen Sie die Konfiguration der Integration erneut, um die Dateiliste zu aktualisieren.

### Lichter reagieren nicht

Wenn die konfigurierten Lichter nicht reagieren, überprüfen Sie, ob die ausgewählten Lichtentitäten korrekt funktionieren und erreichbar sind. Testen Sie die Lichter manuell über die Home Assistant Oberfläche. Stellen Sie sicher, dass alle ausgewählten Lichter die gleichen Funktionen unterstützen, insbesondere wenn Farbwechsel verwendet werden.

### Test-Service funktioniert nicht

Falls der Test-Service nicht funktioniert, überprüfen Sie, ob ein Media Player konfiguriert ist. Stellen Sie sicher, dass eine Audiodatei als Alarmton ausgewählt wurde. Überprüfen Sie die Home Assistant Logs auf Fehlermeldungen unter Einstellungen → System → Protokolle.

## Technische Details

Die Integration verwendet das Home Assistant Event-System für die Kommunikation zwischen Komponenten. Der Test-Service feuert ein internes Event `ha_alarm_pro_test_sound`, das von der Alarm-Entität verarbeitet wird. Die Mehrfach-Licht-Unterstützung erfolgt durch Übergabe einer Liste von Entity-IDs an die Light-Services von Home Assistant, wodurch alle Lichter synchron gesteuert werden.

Die Audiodatei-Erkennung erfolgt durch rekursives Scannen der `/media/` und `/www/` Verzeichnisse beim Laden der Konfiguration. Die Pfade werden automatisch in das korrekte Format konvertiert (`/media/...` oder `/local/...`).

## Support und Feedback

Bei Fragen oder Problemen können Sie die GitHub-Repository-Seite besuchen oder ein Issue erstellen. Für allgemeine Fragen zur Verwendung von Home Assistant konsultieren Sie die offizielle Home Assistant Dokumentation.
