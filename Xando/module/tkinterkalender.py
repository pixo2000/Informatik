import tkinter as tk
from tkinter import messagebox

def ist_schaltjahr(jahr):
    return jahr % 4 == 0 and (jahr % 100 != 0 or jahr % 400 == 0)

def tage_im_monat(monat, jahr):
    if monat == 2:
        return 29 if ist_schaltjahr(jahr) else 28
    elif monat in [4, 6, 9, 11]:
        return 30
    else:
        return 31

def erster_wochentag_im_monat(monat, jahr):
    if monat < 3:
        monat += 12
        jahr -= 1
    k = jahr % 100
    j = jahr // 100
    f = 1 + (13 * (monat + 1)) // 5 + k + k // 4 + j // 4 + 5 * j
    return (f % 7 + 5) % 7

def kalender(monat, jahr):
    monthdays = tage_im_monat(monat, jahr)
    start_day = erster_wochentag_im_monat(monat, jahr)
    
    result = f"{monat}/{jahr}\n"
    result += "Mo Di Mi Do Fr Sa So\n"
    
    result += "   " * start_day
    
    day = 1
    current_day = start_day
    while day <= monthdays:
        result += f"{day:2} "
        day += 1
        current_day += 1
        if current_day == 7:
            result += "\n"
            current_day = 0
    
    return result

def show_calendar():
    try:
        monat = int(entry_month.get())
        jahr = int(entry_year.get())
        if 1 <= monat <= 12:
            calendar_text = kalender(monat, jahr)
            text_calendar.delete(1.0, tk.END)
            text_calendar.insert(tk.END, calendar_text)
        else:
            messagebox.showerror("Fehler", "Bitte geben Sie einen gültigen Monat (1-12) ein.")
    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie gültige Zahlen für Monat und Jahr ein.")

# GUI erstellen
root = tk.Tk()
root.title("Kalender")

frame = tk.Frame(root)
frame.pack(pady=10)

label_month = tk.Label(frame, text="Monat (1-12):")
label_month.grid(row=0, column=0, padx=5)

entry_month = tk.Entry(frame)
entry_month.grid(row=0, column=1, padx=5)

label_year = tk.Label(frame, text="Jahr:")
label_year.grid(row=1, column=0, padx=5)

entry_year = tk.Entry(frame)
entry_year.grid(row=1, column=1, padx=5)

button_show = tk.Button(frame, text="Kalender anzeigen", command=show_calendar)
button_show.grid(row=2, columnspan=2, pady=10)

text_calendar = tk.Text(root, width=20, height=8)
text_calendar.pack(pady=10)

root.mainloop()