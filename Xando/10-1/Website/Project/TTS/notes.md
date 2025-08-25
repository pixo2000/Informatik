# Theißtalschule Website - Redesign

## 📋 Projektübersicht

Modernisierte Version der Theißtalschule Website mit verbessertem Design, vereinfachter Navigation, Dark Mode und separaten Unterseiten.

## 🎯 Verbesserungen

### Design
- **Moderne Optik**: Sauberes, minimalistisches Design
- **Dark Mode**: Umschaltbarer Dunkelmodus mit Speicherung der Präferenz
- **Responsive**: Optimiert für alle Bildschirmgrößen
- **Bessere Typografie**: Verbesserte Lesbarkeit
- **Konsistente Farbpalette**: Professionelle Farbgebung

### Navigation
- **Separate Seiten**: Jede Sektion hat eine eigene Unterseite
- **Verbessertes Mobile-Menü**: Slide-in Navigation mit Overlay
- **Intuitive Struktur**: Logische Informationsarchitektur
- **Smooth Scrolling**: Flüssige Navigation zwischen Bereichen
- **Dark Mode Toggle**: Einfacher Wechsel zwischen Hell/Dunkel

### Inhalt
- **Detaillierte Unterseiten**: Ausführliche Informationen pro Bereich
- **Fokussiert**: Wichtigste Informationen prominent dargestellt
- **Interaktive Kalender**: Filterfunktionen für Termine
- **Umfangreiche Kontaktseite**: Verschiedene Ansprechpartner und Informationen

## 🏗️ Technische Struktur

```
TTS/
├── client/
│   ├── index.html          # Hauptseite
│   ├── schule.html         # Über die Schule
│   ├── termine.html        # Terminkalender
│   ├── grundschule.html    # Grundschule
│   ├── sekundarstufe.html  # Sekundarstufe
│   ├── kontakt.html        # Kontakt
│   ├── style.css           # Styling mit Dark Mode
│   └── script.js           # Interaktivität
├── server/
│   └── main.py             # Entwicklungsserver
└── notes.md               # Diese Dokumentation
```

## 🚀 Starten

1. **Server starten**:
   ```bash
   cd server
   python main.py
   ```

2. **Browser öffnet sich automatisch** auf `http://localhost:8000`

## 📱 Features

### Header
- Fixiertes Menü mit Logo
- Responsive Navigation mit Slide-in Menü
- Dark Mode Toggle Button
- Aktive Seitenmarkierung

### Dark Mode
- **Automatische Erkennung**: Folgt System-Präferenz
- **Manueller Toggle**: Über Schaltfläche in der Navigation
- **Persistente Speicherung**: Einstellung wird gespeichert
- **Smooth Transitions**: Sanfte Übergänge zwischen Modi

### Mobile Navigation
- **Slide-in Menu**: Von rechts einfahrendes Menü
- **Overlay Background**: Dunkler Hintergrund
- **Hamburger Animation**: Wechsel zwischen ☰ und ✕
- **Body Scroll Lock**: Verhindert Scrollen bei offenem Menü
- **Touch-friendly**: Große Klickbereiche

### Seiten-spezifische Features

#### Schule (schule.html)
- Werte-Karten mit Hover-Effekten
- Schulformen-Übersicht
- Statistiken-Sidebar
- Schnellkontakt-Bereich

#### Termine (termine.html)
- Monatliche Terminübersicht
- Filterbare Termine nach Kategorien
- Farbkodierte Event-Types
- Ferienübersicht
- Download-Bereich

#### Grundschule (grundschule.html)
- Klassenstufen-Übersicht
- Betreuungsangebote
- Einschulungsinformationen
- Feature-Karten mit Icons

#### Sekundarstufe (sekundarstufe.html)
- Drei Schulzweige detailliert
- Fächer-Übersicht
- Berufsorientierung
- AG-Angebote

#### Kontakt (kontakt.html)
- Umfangreiches Kontaktformular
- Ansprechpartner-Liste
- Öffnungszeiten
- Anfahrtsinformationen

## 💻 JavaScript Features

- **Dark Mode Management**: Automatische/manuelle Umschaltung
- **Mobile Navigation**: Erweiterte Menü-Funktionalität
- **Form Validation**: Umfangreiche Formular-Validierung
- **Notification System**: Benutzer-Feedback mit verschiedenen Typen
- **Scroll Animations**: Elemente erscheinen beim Scrollen
- **Calendar Filters**: Termine nach Kategorien filtern
- **Theme Persistence**: Speicherung der Dark Mode Präferenz

## 🎨 CSS Features

- **CSS Custom Properties**: Dynamische Farbpalette für Dark Mode
- **Advanced Grid Layouts**: Komplexe, responsive Layouts
- **Smooth Transitions**: Animierte Übergänge zwischen Zuständen
- **Mobile-first Design**: Responsive Breakpoints
- **Modern Shadows & Effects**: Tiefeneffekte und Hover-States

## 📱 Responsive Design

### Desktop (>768px)
- Vollständige Navigation in der Kopfzeile
- Zwei-/Drei-Spalten-Layouts
- Hover-Effekte und Animationen

### Tablet (768px-480px)
- Angepasste Grid-Layouts
- Reduzierte Spaltenanzahl
- Touch-optimierte Interaktionen

### Mobile (<480px)
- Slide-in Navigation
- Einspaltige Layouts
- Große Touch-Targets
- Optimierte Formulare

## 🌗 Dark Mode Implementation

### Automatische Erkennung
```css
:root {
  /* Light mode variables */
}

[data-theme="dark"] {
  /* Dark mode variables */
}
```

### JavaScript Integration
- Erkennung der System-Präferenz
- Toggle-Funktionalität
- LocalStorage-Persistierung
- Smooth Theme-Wechsel

## 📋 TODO / Erweiterungen

- [x] Separate Unterseiten erstellen
- [x] Dark Mode implementieren
- [x] Mobile Navigation verbessern
- [x] Terminkalender mit Filtern
- [x] Umfangreiche Kontaktseite
- [ ] Inhalte aus originaler Website übertragen
- [ ] Echtes Kontaktformular-Backend
- [ ] Suchfunktion über alle Seiten
- [ ] SEO-Optimierung
- [ ] Accessibility-Verbesserungen
- [ ] Performance-Optimierung
- [ ] PWA-Funktionalität

## 🎯 Zielgruppen

1. **Eltern**: Detaillierte Informationen über Schulangebote
2. **Schüler**: Termine, AGs und Aktivitäten
3. **Lehrer**: Einfacher Zugang zu Ressourcen
4. **Interessierte**: Umfassender Überblick über die Schule

## 📊 Verbesserungen vs. Original

| Aspekt | Original | Neu |
|--------|----------|-----|
| Menüpunkte | 50+ | 6 Hauptseiten |
| Ladezeit | Langsam | Schnell |
| Mobile | Schlecht | Optimiert |
| Design | Veraltet | Modern + Dark Mode |
| Navigation | Verwirrend | Intuitive Unterseiten |
| Benutzerfreundlichkeit | Niedrig | Hoch |

## 🔧 Technische Details

### Dark Mode Variablen
- Automatische Farbpaletten-Umschaltung
- Konsistente Farbschemata
- Smooth Transitions zwischen Modi

### Mobile Navigation
- CSS Grid für flexible Layouts
- Transform-Animationen für Slide-Effekte
- Z-Index Management für Overlay

### Form Handling
- Umfangreiche Client-side Validierung
- Benutzerfreundliche Fehlermeldungen
- Responsive Formular-Layouts

Die Website ist jetzt deutlich moderner, benutzerfreundlicher und bietet eine bessere User Experience mit Dark Mode und verbesserter mobiler Navigation.
