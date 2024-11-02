import customtkinter as ctk
from config import map_names
from game import instant_quit  # Import the instant_quit function

class CustomApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.after_ids = []
        self.game_running = False  # Add a flag to check if the game is running
        self.running = True  # Add a flag to control the game loop

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
        if not app.game_running:  # Check if the game is already running
            app.game_running = True
            start_button.pack_forget()  # Remove the start button
            start_game_func(selected_map.get(), start_button, app)  # Pass the selected map, start button, and app

    def on_closing():
        instant_quit(app)  # Call the instant_quit function
        app.quit()  # End the mainloop
        app.cancel_all_after()  # Stop all scheduled after-events
        app.destroy()  # Close the GUI

    map_label = ctk.CTkLabel(app, text="Select Map:")
    map_label.pack(pady=10)

    map_option_menu = ctk.CTkOptionMenu(app, variable=selected_map, values=map_names)
    map_option_menu.pack(pady=10)

    start_button = ctk.CTkButton(app, text="Start Game", command=start_game)
    start_button.pack(pady=20)

    quit_button = ctk.CTkButton(app, text="Quit", command=on_closing)
    quit_button.pack(pady=10)

    app.protocol("WM_DELETE_WINDOW", on_closing)  # Properly close the GUI
    app.mainloop()