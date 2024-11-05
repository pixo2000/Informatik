import customtkinter as ctk
import math
import shutil
from tkinter import messagebox, font


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
        line = " " * (stars - count) + "*" * (2 * count - 1)
        result += center_line_in_console(line, console_width) + "\n"
        count += 1

    return result


def aufgabe3(stars): # is eigentlich die falsche formel. ungenauigkeit in zeile 1 und ende is deshalb
    result = ""
    diameter = 2 * stars + 1
    console_width = get_console_width()

    for i in range(diameter):
        line = ""
        for j in range(diameter):
            if math.sqrt((i - stars) ** 2 + (j - stars) ** 2) <= stars:
                line += "* "
            else:
                line += "  "
        centered_line = center_line_in_console(line, console_width)
        result += centered_line + "\n"

    return result


def show_output(*args):
    global width_var, height_var, font_var
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
        if 'width_var' not in globals() or 'height_var' not in globals():
            width_var = ctk.StringVar(value="300")
            height_var = ctk.StringVar(value="300")
            font_var = ctk.StringVar(value="TkDefaultFont")
        adjust_console_size(output, width_var, height_var, font_var.get())  # Hier das automatische Anpassen aufrufen
    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie gültige Zahlen ein.")


def adjust_console_size(output, width_var, height_var, selected_font):
    lines = output.split("\n")
    max_line_length = max(len(line) for line in lines)
    num_lines = len(lines)

    min_width = int(width_var.get())
    min_height = int(height_var.get())

    # Get the font metrics for the selected font
    fnt = font.Font(family=selected_font, size=12)
    char_width = fnt.measure("0")  # Average width of a character

    # Calculate the new width in pixels
    new_width_pixels = max(min_width * char_width, max_line_length * char_width)
    new_height = max(min_height, num_lines)

    # Convert width from pixels to characters
    new_width_chars = max(min_width, int(new_width_pixels / char_width))

    # Console size adjustment
    text_output.configure(width=new_width_chars, height=new_height)

    # Update the debug window settings if they exist
    width_var.set(str(new_width_chars))
    height_var.set(str(new_height))


def open_debug_window(event=None):
    global width_var, height_var, font_var

    debug_window = ctk.CTkToplevel(root)
    debug_window.title("Debug Einstellungen")
    debug_window.geometry("400x400")

    label_font = ctk.CTkLabel(debug_window, text="Schriftart:")
    label_font.pack(pady=5)

    available_fonts = list(font.families())
    font_var = ctk.StringVar(value="TkDefaultFont")
    dropdown_font = ctk.CTkOptionMenu(debug_window, variable=font_var, values=available_fonts)
    dropdown_font.pack(pady=5)

    label_width = ctk.CTkLabel(debug_window, text="Breite:")
    label_width.pack(pady=5)

    width_var = ctk.StringVar(value="300")
    entry_width = ctk.CTkEntry(debug_window, textvariable=width_var)
    entry_width.pack(pady=5)

    label_height = ctk.CTkLabel(debug_window, text="Höhe:")
    label_height.pack(pady=5)

    height_var = ctk.StringVar(value="300")
    entry_height = ctk.CTkEntry(debug_window, textvariable=height_var)
    entry_height.pack(pady=5)

    def apply_settings(*args):
        new_font = font_var.get()
        text_output.configure(font=(new_font, 12))
        show_output()

    def reset_settings():
        font_var.set("TkDefaultFont")
        width_var.set("300")
        height_var.set("300")

    font_var.trace_add("write", apply_settings)
    width_var.trace_add("write", apply_settings)
    height_var.trace_add("write", apply_settings)

    button_reset = ctk.CTkButton(debug_window, text="Reset", command=reset_settings)
    button_reset.pack(pady=5)

    button_show_output = ctk.CTkButton(debug_window, text="Show Output", command=show_output)
    button_show_output.pack(pady=5)


root = ctk.CTk()
root.title("Sternchen")

frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, side="top")

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

text_output = ctk.CTkTextbox(root, width=300, height=300, font=("Courier", 12))
text_output.pack(pady=20, padx=20, side="top")

root.bind('<F12>', open_debug_window)

root.mainloop()