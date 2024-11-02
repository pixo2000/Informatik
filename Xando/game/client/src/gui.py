import customtkinter as ctk
from config import map_names


class CustomApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.after_ids = []

    def custom_after(self, delay, callback):
        after_id = self.after(delay, callback)
        self.after_ids.append(after_id)
        return after_id

    def cancel_all_after(self):
        for after_id in self.after_ids:
            self.after_cancel(after_id)
        self.after_ids.clear()


def create_gui(start_game_func):
    app = CustomApp()
    app.geometry("400x300")
    app.title("2D Shooter Launcher")

    selected_map = ctk.StringVar(value=map_names[0])

    def start_game():
        app.quit()  # Beende die mainloop, um laufende tkinter Ereignisse zu stoppen
        app.cancel_all_after()  # Stoppe alle geplanten after-Events
        app.destroy()  # Schließe die GUI
        start_game_func(selected_map.get())  # Pass the selected map

    def on_closing():
        app.quit()  # Beende die mainloop
        app.cancel_all_after()  # Stoppe alle geplanten after-Events
        app.destroy()  # Schließe die GUI

    start_button = ctk.CTkButton(app, text="Start Game", command=start_game)
    start_button.pack(pady=20)

    map_label = ctk.CTkLabel(app, text="Select Map:")
    map_label.pack(pady=10)

    map_option_menu = ctk.CTkOptionMenu(app, variable=selected_map, values=map_names)
    map_option_menu.pack(pady=10)

    app.protocol("WM_DELETE_WINDOW", on_closing)  # Schließe die GUI korrekt
    app.mainloop()