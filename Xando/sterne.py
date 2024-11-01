# aufgabe 1:
# halt das mit sternen

# aufgabe 2:
# als pyramiede

# aufgabe 3:
# kreis mit sternen

import tkinter as tk
from tkinter import messagebox

# Get Star Number
def getstars():
    stars = int(input("Wie viele Sterne? "))
    if stars = 0:
        messagebox.showerror("Fehler", "Bitte gib eine Zahl über 1 ein, um einen Output zu bekommen")
        exit()
    else:
        return stars

# Aufgabe 1:
def aufgabe1(stars):
    result = ""
    count = 1

    while counter <= stars:
        result += "*" * counter
        counter += 1
    
    return result

# Aufgabe 2:
def aufgabe2(stars):
    result += ""
    count = 1

    while counter <= stars:
        result = " " * (stars - counter) + "*" * (2 * counter - 1)
        counter += 1

    return result

# Aufgabe 3:
# hier code hin

# GUI
root = tk.Tk()
root.title("Kalender")

frame = tk.Frame(root)
frame.pack(pady=10)

label_stars = tk.Label(frame, text="Sterne:")
label_stars.grid(row=0, column=0, padx=5)

entry_stars = tk.Entry(frame)
entry_stars.grid(row=0, column=1, padx=5)

label_task = tk.Label(frame, text="Aufgabe:")
label_task.grid(row=0, column=0, padx=5)

entry_task = tk.Entry(frame)
entry_task.grid(row=0, column=1, padx=5)