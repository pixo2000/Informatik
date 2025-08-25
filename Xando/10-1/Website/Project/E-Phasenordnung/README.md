# E-Phasen Schülerzuordnung

Ein lokales Tool zur Zuordnung der Schüler in neue Klassen in der E-Phase.

## Funktionen

- ✅ **Schülerdaten erfassen** mit allen relevanten Feldern
- ✅ **Prioritätssystem** - je später das Feld nach "Abgabedatum", desto geringere Priorität
- ✅ **Suchfunktion** und Filter in der Übersicht
- ✅ **Server-API** zum Hosten der Daten
- ✅ **Fallback auf lokale Speicherung** wenn Server nicht erreichbar
- ✅ **Validierung** der Fächerkombinationen
- ✅ **Export-/Druckfunktion**
- ✅ **Automatische Klassenzuordnung** mit intelligentem Algorithmus
- ✅ **Konfliktdetektion** für Freundschaften und Fächerkombinationen
- ✅ **Klassenexport** und Druckfunktion für Zuordnungen
- ✅ **Manuelle Klassenbearbeitung** mit Drag-and-Drop Interface
- ✅ **Automatische Datensicherung** alle 5 Minuten mit Backup-System
- ✅ **Datenwiederherstellung** aus Backups bei Server-Ausfällen

## Felder

### Pflichtfelder (hohe Priorität)
- Name, Vorname
- Geschlecht (männlich/weiblich)
- Rechtzeitig abgegeben (Checkbox)

### Fachwahlfelder (mittlere Priorität)
- 2. Fremdsprache (Französisch, Latein, Spanisch)
- Musisches Fach (Musik, Kunst)
- Religiöses Fach (Katholisch, Evangelisch, Ethik)
- Freies Fach (Erdkunde, Philosophie, Informatik, Erdkunde Bilingual, Spanisch 3. FS, Latein 3. FS)

### Soziale Felder (niedrige Priorität)
- Freund 1 (optional)
- Freund 2 (optional)

## Installation

### Server starten

1. **Python-Abhängigkeiten installieren:**
   ```powershell
   cd server
   pip install -r requirements.txt
   ```

2. **Server starten:**
   ```powershell
   python main.py
   ```

   Der Server läuft dann auf `http://localhost:5000`

### Client öffnen

1. **Webseite öffnen:**
   Öffnen Sie `client/index.html` in Ihrem Browser

2. **Oder über lokalen Server:**
   ```powershell
   cd client
   python -m http.server 8000
   ```
   Dann `http://localhost:8000` im Browser öffnen

## Prioritätssystem

Das System berechnet automatisch Prioritäten basierend auf:

1. **Rechtzeitig abgegeben**: +100 Punkte
2. **2. Fremdsprache**: +90 Punkte  
3. **Musisches Fach**: +80 Punkte
4. **Religiöses Fach**: +70 Punkte
5. **Freies Fach**: +60 Punkte
6. **Freund 1**: +50 Punkte
7. **Freund 2**: +40 Punkte

Schüler werden in der Übersicht nach Priorität sortiert angezeigt.

## Validierungsregeln

- **Spanisch**: Kann nicht gleichzeitig 2. und 3. Fremdsprache sein
- **Latein**: Kann nicht gleichzeitig 2. und 3. Fremdsprache sein

## API Endpunkte

### Schüler
- `GET /api/students` - Alle Schüler abrufen
- `POST /api/students` - Neuen Schüler hinzufügen
- `PUT /api/students/<id>` - Schüler aktualisieren
- `DELETE /api/students/<id>` - Schüler löschen
- `GET /api/students/stats` - Statistiken abrufen

### Klassenzuordnung
- `POST /api/assignments` - Automatische Klassenzuordnung erstellen
- `GET /api/assignments` - Letzte Zuordnung abrufen
- `PUT /api/assignments` - Klassenzuordnung manuell bearbeiten
- `POST /api/assignments/student/<id>/move` - Schüler zwischen Klassen verschieben

### System
- `GET /api/health` - Health Check

## Offline-Modus

Falls der Server nicht erreichbar ist, arbeitet die Anwendung automatisch mit lokaler Speicherung (localStorage) und synchronisiert sich beim nächsten Server-Start.

## Manuelle Klassenbearbeitung

Im **Klassenzuordnung** Tab können Sie:

- 📋 **Bestehende Zuordnungen laden** und bearbeiten
- 🖱️ **Drag-and-Drop Interface** zum Verschieben von Schülern zwischen Klassen
- 📊 **Live-Statistiken** für jede Klasse (Geschlechterverteilung, Fächer)
- 💾 **Änderungen speichern** mit Validierung
- ⚠️ **Unsaved Changes Warning** beim Verlassen der Seite

### Bedienung:
1. Wechseln Sie zum **Klassenzuordnung** Tab
2. Klicken Sie **Zuordnungen laden** um bestehende Klassenzuordnungen zu laden
3. Ziehen Sie Schüler zwischen den Klassen per Drag & Drop
4. Speichern Sie Ihre Änderungen mit **Änderungen speichern**

## Automatische Datensicherung

Der Server erstellt automatisch Backups aller wichtigen Daten:

- 💾 **Automatische Backups** alle 5 Minuten
- 📁 **Backup-Ordner**: `backups/` mit Zeitstempel
- 🔄 **Automatische Wiederherstellung** bei Datenverlust
- 🗑️ **Automatische Bereinigung** - behält nur die letzten 10 Backups
- 📝 **Separate Backups** für Schülerdaten und Klassenzuordnungen

### Backup-Dateien:
- `students_YYYYMMDD_HHMMSS.json` - Schülerdaten
- `assignments_YYYYMMDD_HHMMSS.json` - Klassenzuordnungen

## Keyboard Shortcuts

- `Ctrl+S` - Formular speichern (auf Eingabe-Tab)
- `Ctrl+F` - Suchfeld fokussieren
- `Esc` - Bearbeitung abbrechen
