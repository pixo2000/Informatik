import pyautogui
import time

def open_calendar():
    # Öffne den Windows-Kalender (normalerweise durch Klicken auf die Uhr in der Taskleiste)
    # Die Position der Uhr in der Taskleiste kann je nach Bildschirmauflösung variieren.
    # Hier wird eine Beispielposition verwendet. Passe sie bei Bedarf an.
    pyautogui.click(x=1820, y=1060)  # Beispielposition für 1920x1080 Auflösung
    time.sleep(1)  # Warte, bis der Kalender geöffnet ist

def navigate_to_month_year(monat, jahr):
    current_year = time.localtime().tm_year
    current_month = time.localtime().tm_mon

    # Navigiere zu dem gewünschten Jahr
    year_diff = jahr - current_year
    if year_diff != 0:
        pyautogui.click(x=960, y=540)  # Beispielposition für das Jahr im Kalender
        time.sleep(0.5)
        for _ in range(abs(year_diff)):
            if year_diff > 0:
                pyautogui.click(x=1000, y=540)  # Beispielposition für "Nächstes Jahr"
            else:
                pyautogui.click(x=920, y=540)  # Beispielposition für "Vorheriges Jahr"
            time.sleep(0.5)

    # Navigiere zu dem gewünschten Monat
    month_diff = monat - current_month
    for _ in range(abs(month_diff)):
        if month_diff > 0:
            pyautogui.click(x=1000, y=600)  # Beispielposition für "Nächster Monat"
        else:
            pyautogui.click(x=920, y=600)  # Beispielposition für "Vorheriger Monat"
        time.sleep(0.5)

# Eingabe von Monat und Jahr über die Konsole
monat = int(input("Bitte geben Sie den Monat ein (1-12): "))
jahr = int(input("Bitte geben Sie das Jahr ein: "))

open_calendar()
navigate_to_month_year(monat, jahr)