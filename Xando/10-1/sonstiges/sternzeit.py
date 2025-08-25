# # 1000 sartada units = 1 earth year
# # n = anzahl der tage im jahr also 365 bzw 366 für schaltjahre
# # b = das jahr in der berechnung anfängt(2005 = 58000.00/2323 = 00000.00)
# # c = die sternzeit zum jahr 'b'
# # m = nummer der tage vom monat: Januar = 0, Februar = 31(bei allen weiteren +1 rechnen wenn es ein schaltjahr ist)
# #     März = 59, April = 90, Mai = 120, Juni = 151, Juli = 181, August = 212, September = 243, Oktober = 273,
# #     November = 304, Dezember = 334
# # d = tag im monat
# # y = jahr
# #
# # Beispiel: 23. Mai 2008 wird zu -> n = 366; b = 2005; c = 58000.00; m = 121 (120, +1 wegen Schaltjahr); d = 23; y = 2008. 
# #
# # Formel: c + (1000*(y-b)) + ((1000/n)*(m + d -1))
# # Sternzeit immer 2 nachkommastellen
# #
# # am ende dann auch anders rum rechnen siehe link
# #
# #
# # s = schaltjahrnummer
# # s2 = für monat ob +1 sein soll
# # https://www.wikihow.com/Calculate-Stardates

# b = input("Wann fängt die rechnung an? 2005/2323?: ")
# m = input("Welchen Monat haben wir?: ")
# d = input("Welchen Tag haben wir?: ")
# y = input("Welches Jahr haben wir?: ")

# if 


# if m = "Januar":
#     m = 0
# if m = "Februar":
#     m= 31
# if m = "März":
#     m = 59 + s2


# # Schaltjahrrechnung
# while y > 4:
#     y - 4
#     s + 1
#     if y < 4:


# # jahr 2008 war schaltjahr.
# # beispiel 2034:
# # 2034, 2030, 2026, 2022, 2018, 2014, 2010

# # immer zieljahr minus erstes schaltjahr und dann berechnung sonst kommt zu viel raus

# # für s2 checken ob generell was übrig bleibt und wenn ja auf true setzen zum späteren abfragen

# # wann startet der aktuelle kalender
# # -> erst mal wissen wie der heisst
# # genauere schaltjahre(nicht nur alle 4 jahre sondern auch alle 100 ig)

import tkinter as tk
from tkinter import messagebox

def ist_schaltjahr(jahr):
    return jahr % 4 == 0 and (jahr % 100 != 0 or jahr % 400 == 0)

def tage_im_monat(monat, jahr):
    tage = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if ist_schaltjahr(jahr) and monat > 1:
        return tage[monat] + 1
    return tage[monat]

def sternzeit_zu_datum(sternzeit, b):
    if b == 2005:
        c = 58000.00
    else:
        c = 0.00

    # Berechne das Jahr
    jahr = b + int((sternzeit - c) // 1000)
    
    # Berechne die Anzahl der Tage im Jahr
    n = 366 if ist_schaltjahr(jahr) else 365
    
    # Berechne den Tag im Jahr
    rest = (sternzeit - c) % 1000
    tag_im_jahr = int((rest * n) // 1000)
    
    # Finde den Monat und Tag
    tage = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if ist_schaltjahr(jahr):
        tage = [t + 1 if i > 1 else t for i, t in enumerate(tage)]
    
    monat = 0
    for i in range(len(tage) - 1):
        if tage[i] <= tag_im_jahr < tage[i + 1]:
            monat = i
            tag = tag_im_jahr - tage[i] + 1
            break
    else:
        monat = 11
        tag = tag_im_jahr - tage[11] + 1
    
    return tag, monat + 1, jahr

def datum_zu_sternzeit(b, m, d, y):
    # Bestimme die Anzahl der Tage im Jahr
    n = 366 if ist_schaltjahr(y) else 365
    
    # Bestimme die Sternzeit zum Jahr 'b'
    c = 58000.00 if b == 2005 else 0.00
    
    # Bestimme die Nummer der Tage vom Monat
    m = tage_im_monat(m, y)
    
    # Berechne die Sternzeit
    sternzeit = c + (1000 * (y - b)) + ((1000 / n) * (m + d - 1))
    
    return round(sternzeit, 2)

def berechne_sternzeit():
    try:
        b = int(entry_b.get())
        monat = entry_monat.get()
        d = int(entry_tag.get())
        y = int(entry_jahr.get())

        monate = {
            "Januar": 0,
            "Februar": 1,
            "März": 2,
            "April": 3,
            "Mai": 4,
            "Juni": 5,
            "Juli": 6,
            "August": 7,
            "September": 8,
            "Oktober": 9,
            "November": 10,
            "Dezember": 11
        }

        m = monate[monat]

        result = datum_zu_sternzeit(b, m, d, y)
        messagebox.showinfo("Ergebnis", f"Die Sternzeit für das Datum {d}. {monat} {y} ist: {result}")
    except Exception as e:
        messagebox.showerror("Fehler", str(e))

def berechne_datum():
    try:
        sternzeit = float(entry_sternzeit.get())
        b = int(entry_b.get())

        tag, monat, jahr = sternzeit_zu_datum(sternzeit, b)
        monate = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
        messagebox.showinfo("Ergebnis", f"Das Datum für die Sternzeit {sternzeit} ist: {tag}. {monate[monat - 1]} {jahr}")
    except Exception as e:
        messagebox.showerror("Fehler", str(e))

# GUI erstellen
root = tk.Tk()
root.title("Sternzeit Rechner")

frame = tk.Frame(root)
frame.pack(pady=10)

label_b = tk.Label(frame, text="Startjahr (2005/2323):")
label_b.grid(row=0, column=0, padx=5)
entry_b = tk.Entry(frame)
entry_b.grid(row=0, column=1, padx=5)

label_monat = tk.Label(frame, text="Monat (Januar, Februar, ...):")
label_monat.grid(row=1, column=0, padx=5)
entry_monat = tk.Entry(frame)
entry_monat.grid(row=1, column=1, padx=5)

label_tag = tk.Label(frame, text="Tag:")
label_tag.grid(row=2, column=0, padx=5)
entry_tag = tk.Entry(frame)
entry_tag.grid(row=2, column=1, padx=5)

label_jahr = tk.Label(frame, text="Jahr:")
label_jahr.grid(row=3, column=0, padx=5)
entry_jahr = tk.Entry(frame)
entry_jahr.grid(row=3, column=1, padx=5)

button_sternzeit = tk.Button(frame, text="Berechne Sternzeit", command=berechne_sternzeit)
button_sternzeit.grid(row=4, columnspan=2, pady=10)

label_sternzeit = tk.Label(frame, text="Sternzeit:")
label_sternzeit.grid(row=5, column=0, padx=5)
entry_sternzeit = tk.Entry(frame)
entry_sternzeit.grid(row=5, column=1, padx=5)

button_datum = tk.Button(frame, text="Berechne Datum", command=berechne_datum)
button_datum.grid(row=6, columnspan=2, pady=10)

root.mainloop()