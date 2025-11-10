# Beitragen zum NFC Alarm System

Vielen Dank für Ihr Interesse, zum NFC Alarm System beizutragen! Diese Anleitung hilft Ihnen dabei, einen Beitrag zu leisten.

## Entwicklungsumgebung einrichten

### Voraussetzungen

- Python 3.11 oder höher
- Home Assistant Entwicklungsumgebung
- Git

### Lokale Installation für Entwicklung

1. Forken Sie das Repository auf GitHub
2. Klonen Sie Ihr Fork:
   ```bash
   git clone https://github.com/IhrUsername/nfc_alarm_system.git
   cd nfc_alarm_system
   ```

3. Erstellen Sie einen symbolischen Link in Ihrer Home Assistant Installation:
   ```bash
   ln -s $(pwd)/custom_components/nfc_alarm_system ~/.homeassistant/custom_components/nfc_alarm_system
   ```

4. Starten Sie Home Assistant neu

## Code-Stil

- Folgen Sie PEP 8 für Python-Code
- Verwenden Sie Type Hints wo möglich
- Schreiben Sie aussagekräftige Commit-Nachrichten
- Kommentieren Sie komplexen Code auf Deutsch oder Englisch

## Pull Requests

1. Erstellen Sie einen neuen Branch für Ihre Änderung:
   ```bash
   git checkout -b feature/meine-neue-funktion
   ```

2. Machen Sie Ihre Änderungen und committen Sie:
   ```bash
   git add .
   git commit -m "Füge neue Funktion hinzu: ..."
   ```

3. Pushen Sie zu Ihrem Fork:
   ```bash
   git push origin feature/meine-neue-funktion
   ```

4. Erstellen Sie einen Pull Request auf GitHub

## Fehler melden

Wenn Sie einen Fehler finden:

1. Überprüfen Sie, ob der Fehler bereits gemeldet wurde
2. Erstellen Sie ein neues Issue mit:
   - Beschreibung des Problems
   - Schritte zur Reproduktion
   - Erwartetes Verhalten
   - Tatsächliches Verhalten
   - Home Assistant Version
   - Relevante Logs

## Lizenz

Durch Ihren Beitrag stimmen Sie zu, dass Ihre Änderungen unter der MIT-Lizenz veröffentlicht werden.
