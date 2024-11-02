# Aufgabe 1:
# Auflistung mit Sternen

# Aufgabe 2:
# als Pyramide

# Aufgabe 3:
# Kreis mit Sternen

import customtkinter as ctk
from tkinter import messagebox, ttk
import math
import shutil

def get_console_width():
    return shutil.get_terminal_size().columns

def center_line_in_console(line, console_width):
    total_leading_spaces = (console_width - len(line)) // 2
    return " " * total_leading_spaces + line.rstrip()

def aufgabe1(stars):
    result = ""
    count = 1

    while count <= stars:
        result += "*" * count + "\n"
        count += 1

    return result

def aufgabe2(stars):
    result = ""
    count = 1
    console_width = get_console_width()

    while count <= stars:
        line = "  " * (stars - count) + "*" * (2 * count - 1)
        result += center_line_in_console(line, console_width) + "\n"
        count += 1

    return result

def aufgabe3(stars):
    result = ""
    diameter = 2 * stars + 1
    console_width = get_console_width()

    for i in range(diameter):
        line = ""
        for j in range(diameter):
            if math.sqrt((i - stars) ** 2 + (j - stars) ** 2) <= stars:
                line += "*"
            else:
                line += " "
        centered_line = center_line_in_console(line, console_width)
        result += centered_line + "\n"

    return result

def show_output(*args):
    try:
        stars_str = entry_stars.get()
        if not stars_str:
            text_output.delete(1.0, ctk.END)
            return

        stars = int(stars_str)
        if stars < 1:
            messagebox.showerror("Fehler", "Bitte gib eine Zahl größer als 0 ein, um einen Output zu bekommen")
            return

        task = int(option_task.get())
        if task == 1:
            output = aufgabe1(stars)
        elif task == 2:
            output = aufgabe2(stars)
        elif task == 3:
            output = aufgabe3(stars)
        else:
            messagebox.showerror("Fehler", "Bitte gib eine gültige Aufgabe (1, 2 oder 3) ein.")
            return

        text_output.delete(1.0, ctk.END)
        text_output.insert(ctk.END, output)
    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie gültige Zahlen ein.")

def toggle_dev_tools():
    if dev_tools_var.get() == 1:
        dev_tools_frame.pack(side="left", padx=10)
    else:
        dev_tools_frame.pack_forget()

def apply_console_settings():
    try:
        new_width = int(entry_console_width.get())
        new_height = int(entry_console_height.get())
        new_font = entry_console_font.get()
        text_output.configure(width=new_width, height=new_height, font=(new_font, 12))
        show_output()  # Regenerate the output when settings are applied
    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie gültige Zahlen ein.")

def reset_console_settings():
    entry_console_width.delete(0, ctk.END)
    entry_console_width.insert(0, "300")
    entry_console_height.delete(0, ctk.END)
    entry_console_height.insert(0, "300")
    entry_console_font.set("TkDefaultFont")
    text_output.configure(width=300, height=300, font=("TkDefaultFont", 12))

def update_button_layout():
    for widget in frame.winfo_children():
        widget.pack_forget()
    if button_layout_var.get() == 1:  # Horizontal
        dev_tools_checkbox.pack(side="left", padx=5)
        button_layout_switch.pack(side="left", padx=5)
        label_stars.pack(side="left", padx=5)
        entry_stars.pack(side="left", padx=5)
        label_task.pack(side="left", padx=5)
        option_task.pack(side="left", padx=5)
    else:  # Vertical
        dev_tools_checkbox.pack(pady=5, anchor="w")
        button_layout_switch.pack(pady=5, anchor="w")
        label_stars.pack(pady=5)
        entry_stars.pack(pady=5)
        label_task.pack(pady=5)
        option_task.pack(pady=5)
        if dev_tools_var.get() == 1:
            dev_tools_frame.pack(side="left", padx=10)

    for widget in console_settings_frame.winfo_children():
        widget.pack_forget()
    if button_layout_var.get() == 1:  # Horizontal
        label_console_width.pack(side="left", padx=5)
        entry_console_width.pack(side="left", padx=5)
        label_console_height.pack(side="left", padx=5)
        entry_console_height.pack(side="left", padx=5)
        label_console_font.pack(side="left", padx=5)
        entry_console_font.pack(side="left", padx=5)
        button_apply_settings.pack(side="left", padx=5)
        button_reset_settings.pack(side="left", padx=5)
    else:  # Vertical
        label_console_width.pack(pady=5)
        entry_console_width.pack(pady=5)
        label_console_height.pack(pady=5)
        entry_console_height.pack(pady=5)
        label_console_font.pack(pady=5)
        entry_console_font.pack(pady=5)
        button_apply_settings.pack(pady=5)
        button_reset_settings.pack(pady=5)

root = ctk.CTk()
root.title("Sternchen")
root.iconbitmap('star.ico')

frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, side="left")

dev_tools_frame = ctk.CTkFrame(root)
dev_tools_frame.pack(pady=20, padx=20, side="left")
dev_tools_frame.pack_forget()  # Initially hide the dev tools frame

dev_tools_var = ctk.IntVar()
dev_tools_checkbox = ctk.CTkCheckBox(frame, text="Dev-Tools", variable=dev_tools_var, command=toggle_dev_tools)
dev_tools_checkbox.pack(padx=10, pady=10, anchor="w")

button_layout_var = ctk.IntVar(value=0)  # 0 for Vertical, 1 for Horizontal
button_layout_switch = ctk.CTkSwitch(frame, text="Horizontal/Vertical", variable=button_layout_var, onvalue=1, offvalue=0, command=update_button_layout)
button_layout_switch.pack(pady=10, anchor="w")

label_stars = ctk.CTkLabel(frame, text="Sterne:")
label_stars.pack(pady=5)

entry_stars = ctk.CTkEntry(frame)
entry_stars.pack(pady=5)
entry_stars_var = ctk.StringVar()
entry_stars.configure(textvariable=entry_stars_var)
entry_stars_var.trace_add("write", show_output)

label_task = ctk.CTkLabel(frame, text="Aufgabe:")
label_task.pack(pady=5)

option_task = ctk.CTkOptionMenu(frame, values=["1", "2", "3"])
option_task.pack(pady=5)
option_task.set("1")
option_task.configure(command=show_output)

console_settings_frame = ctk.CTkFrame(dev_tools_frame)
console_settings_frame.pack(pady=10, padx=10)

label_console_width = ctk.CTkLabel(console_settings_frame, text="Console Width:")
label_console_width.pack(pady=5)

entry_console_width = ctk.CTkEntry(console_settings_frame)
entry_console_width.pack(pady=5)
entry_console_width.insert(0, "300")

label_console_height = ctk.CTkLabel(console_settings_frame, text="Console Height:")
label_console_height.pack(pady=5)

entry_console_height = ctk.CTkEntry(console_settings_frame)
entry_console_height.pack(pady=5)
entry_console_height.insert(0, "300")

label_console_font = ctk.CTkLabel(console_settings_frame, text="Console Font:")
label_console_font.pack(pady=5)

entry_console_font = ctk.CTkOptionMenu(console_settings_frame, values=["TkDefaultFont", "Arial", "Courier", "Helvetica", "Times"])
entry_console_font.pack(pady=5)
entry_console_font.set("TkDefaultFont")

button_apply_settings = ctk.CTkButton(console_settings_frame, text="Apply Settings", command=apply_console_settings)
button_apply_settings.pack(pady=5)

button_reset_settings = ctk.CTkButton(console_settings_frame, text="Reset Settings", command=reset_console_settings)
button_reset_settings.pack(pady=5)

text_output = ctk.CTkTextbox(root, width=300, height=300, font=("TkDefaultFont", 12))
text_output.pack(pady=20, padx=20)

root.mainloop()