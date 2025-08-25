# RaphCup - Valorant Tournament Platform

Ein vollständiges Tournament-Management-System für Valorant mit E-Mail-Verifizierung, Admin-Panel und Turnier-Anmeldungen.

## Features

- ✅ Benutzer-Registrierung mit E-Mail-Verifizierung
- ✅ Passwort-Reset per E-Mail
- ✅ Admin-Panel für Turnier-Erstellung
- ✅ Turnier-Anmeldungen mit Discord & Valorant-Rang
- ✅ Datums-Abstimmung für Turniere
- ✅ Responsive Design im Valorant-Theme
- ✅ Sichere Session-Verwaltung

## Installation

### 1. Abhängigkeiten installieren

```bash
cd server
pip install -r requirements.txt
```

### 2. E-Mail-Konfiguration

1. Kopiere `.env.example` zu `.env`:
```bash
cp .env.example .env
```

2. Bearbeite `.env` und trage deine Gmail-Daten ein:
```bash
EMAIL_ADDRESS=deine-gmail@gmail.com
EMAIL_PASSWORD=dein-app-passwort
```

**Wichtig**: Für Gmail musst du ein App-Passwort erstellen:
1. Gehe zu [Google Account Settings](https://myaccount.google.com)
2. Sicherheit → 2-Faktor-Authentifizierung aktivieren
3. App-Passwörter → Neues App-Passwort für "RaphCup" erstellen
4. Verwende dieses App-Passwort (nicht dein normales Gmail-Passwort)

### 3. Datenbank initialisieren

```bash
python main.py
```

Die Datenbank wird automatisch beim ersten Start erstellt.

### 4. Admin-Benutzer erstellen

```bash
python setup_admin.py
```

Folge den Anweisungen um den ersten Admin-Account zu erstellen.

## Verwendung

### Server starten

```bash
cd server
python main.py
```

Der Server läuft auf: http://localhost:5000

### Erste Schritte

1. Öffne http://localhost:5000 im Browser
2. Registriere dich mit einer gültigen E-Mail
3. Verifiziere deine E-Mail mit dem Code
4. Logge dich ein
5. Als Admin: Erstelle Turniere im Admin-Panel
6. Als Benutzer: Melde dich für Turniere an

## Dateistruktur

```
RaphCup/
├── client/                 # Frontend-Dateien
│   ├── index.html         # Homepage
│   ├── login.html         # Login-Seite
│   ├── register.html      # Registrierung
│   ├── dashboard.html     # Benutzer-Dashboard
│   ├── admin.html         # Admin-Panel
│   ├── reset-password.html # Passwort-Reset
│   ├── style.css          # Styling
│   └── script.js          # JavaScript
├── server/                # Backend-Dateien
│   ├── main.py           # Haupt-Server
│   ├── config.py         # Konfiguration
│   ├── database.py       # Datenbank-Operationen
│   ├── email_service.py  # E-Mail-Service
│   ├── auth.py           # Authentifizierung
│   ├── setup_admin.py    # Admin-Setup-Script
│   ├── requirements.txt  # Python-Abhängigkeiten
│   ├── .env             # Umgebungsvariablen (nicht in Git)
│   └── .env.example     # Beispiel-Konfiguration
└── README.md
```

## API-Endpunkte

### Authentifizierung
- `POST /api/register` - Benutzer registrieren
- `POST /api/verify` - E-Mail verifizieren
- `POST /api/login` - Einloggen
- `POST /api/logout` - Ausloggen
- `POST /api/forgot-password` - Passwort-Reset anfordern
- `POST /api/reset-password` - Passwort zurücksetzen

### Turniere
- `GET /api/tournaments` - Alle Turniere abrufen
- `POST /api/tournaments` - Turnier erstellen (Admin)
- `POST /api/register_tournament` - Für Turnier anmelden
- `GET /api/user/tournaments` - Eigene Turniere

### Admin
- `GET /api/admin/registrations/<id>` - Turnier-Anmeldungen abrufen

## Sicherheit

- Passwörter werden mit Werkzeug gehasht
- E-Mail-Verifizierung mit zeitlich begrenzten Codes
- Session-basierte Authentifizierung
- CSRF-Schutz durch SameSite-Cookies
- SQL-Injection-Schutz durch Prepared Statements

## Entwicklung

### Lokale Entwicklung

1. Setze `DEBUG=True` in der `.env`-Datei
2. Der Server startet automatisch bei Dateiänderungen neu

### Produktions-Deployment

1. Setze `DEBUG=False` in der `.env`-Datei
2. Ändere `SECRET_KEY` zu einem sicheren Wert
3. Verwende einen Reverse-Proxy (nginx) für statische Dateien
4. Verwende eine Produktions-Datenbank (PostgreSQL)

## Troubleshooting

### E-Mails werden nicht versendet
- Überprüfe Gmail App-Passwort
- Stelle sicher, dass 2FA aktiviert ist
- Prüfe die Konsolen-Ausgabe für Fehlermeldungen

### Datenbank-Fehler
- Lösche `raphcup.db` und starte den Server neu
- Führe `setup_admin.py` erneut aus

### Admin-Zugang verloren
- Führe `setup_admin.py` aus um einen neuen Admin zu erstellen

## Support

Bei Problemen oder Fragen erstelle ein Issue im Repository oder kontaktiere das Entwicklungsteam.

## Lizenz

Dieses Projekt ist für den RaphCup entwickelt worden. Alle Rechte vorbehalten.
