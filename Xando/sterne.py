# aufgabe 1:
# halt das mit sternen

# aufgabe 2:
# als pyramiede

# aufgabe 3:
# kreis mit sternen

import tkinter as tk
from tkinter import messagebox
import math

# Aufgabe 1:
def aufgabe1(stars):
    result = ""
    count = 1

    while count <= stars:
        result += "*" * count
        count += 1
    
    return result

# Aufgabe 2:
def aufgabe2(stars):
    result = ""
    count = 1

    while count <= stars:
        result += " " * (stars - count) + "*" * (2 * count - 1) + "\n"
        count += 1

    return result

# Aufgabe 3:
def aufgabe3(stars):
    result = ""
    i = 0

    while i < (2 * stars) + 1:
        j = 0
        line = ""
        while j < (2 * stars) + 1:
            if math.sqrt((i - stars) ** 2 + (j - stars) ** 2) <= stars:
                line += "*"
            else:
                line += " "
            j += 1
        result += line + "\n"
        i += 1
    
    return result

# GUI
def show_output():
    try:
        stars = int(entry_stars.get())
        if starnumber == 0:
            messagebox.showerror("Fehler", "Bitte gib eine Zahl über 1 ein, um einen Output zu bekommen")

        task = int(entry_task.get())
        if task == 1:
            output = aufgabe1(stars)
        elif task == 2:
            output = aufgabe2(stars)
        elif task == 3:
            output = aufgabe3(stars)
        
        text_calendar.delete(1.0, tk.END)
        text_calendar.insert(tk.END, output)
    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie gültige Zahlen ein.")

root = tk.Tk()
root.title("Sternchen")

frame = tk.Frame(root)
frame.pack(pady=10)

label_stars = tk.Label(frame, text="Sterne:")
label_stars.grid(row=0, column=0, padx=5)

entry_stars = tk.Entry(frame)
entry_stars.grid(row=0, column=1, padx=5)

label_task = tk.Label(frame, text="Aufgabe:")
label_task.grid(row=1, column=0, padx=5)

entry_task = tk.Entry(frame)
entry_task.grid(row=1, column=1, padx=5)

button_show = tk.Button(frame, text="Output anzeigen", command=show_output)
button_show.grid(row=2, columnspan=2, pady=10)

text_calendar = tk.Text(root, width=20, height=11)
text_calendar.pack(pady=10)

root.mainloop()