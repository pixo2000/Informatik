import calendar

def kalender(monat, jahr):
    # Bestimme die Anzahl der Tage im Monat
    monthdays = calendar.monthrange(jahr, monat)[1]
    
    # Erstelle eine Liste der Wochentage für den Monat
    month_calendar = calendar.monthcalendar(jahr, monat)
    
    # Gib den Kalender für den Monat aus
    print(calendar.month_name[monat], jahr)
    print("Mo Di Mi Do Fr Sa So")
    for week in month_calendar:
        print(" ".join(f"{day:2}" if day != 0 else "  " for day in week))

# Beispielaufruf
kalender(10, 2024)