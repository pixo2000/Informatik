import customtkinter as ctk

def create_gui(start_game_func):
    app = ctk.CTk()
    app.geometry("400x300")
    app.title("2D Shooter Settings")

    def start_game():
        app.destroy()  # Close the GUI
        start_game_func()  # Start the game

    start_button = ctk.CTkButton(app, text="Start Game", command=start_game)
    start_button.pack(pady=20)

    app.mainloop()