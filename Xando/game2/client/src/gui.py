import customtkinter as ctk
from config import map_names, host, port
import socket
from tkinter import messagebox

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
            # Check if the server is running
            server_address = (host, port)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect(server_address)
                sock.close()
            except socket.error:
                messagebox.showerror("Connection Error",
                                     "Unable to connect to the server. Please make sure the server is running.")
                return

            start_game() # fix this ig
            start_button.pack_forget()  # Remove the start button
            start_game_func(selected_map.get(), start_button, app)  # Pass the selected map, start button, and app

    def on_closing():
        app.quit()  # End the mainloop
        app.cancel_all_after()  # Stop all scheduled after-events
        app.destroy()  # Close the GUI

    def ping_server():
        led_label.configure(bg_color="red")  # Set LED to red initially
        server_address = (host, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(server_address)
            sock.close()
            led_label.configure(bg_color="green")  # Turn LED green if server is reachable
        except socket.error:
            pass  # LED remains red if server is not reachable
        app.custom_after(10000, ping_server)  # Schedule the next ping in 10 seconds

    map_label = ctk.CTkLabel(app, text="Select Map:")
    map_label.pack(pady=10)

    map_option_menu = ctk.CTkOptionMenu(app, variable=selected_map, values=map_names)
    map_option_menu.pack(pady=10)

    quit_button = ctk.CTkButton(app, text="Quit", command=on_closing)
    quit_button.pack(pady=10)

    start_button = ctk.CTkButton(app, text="Start Game", command=start_game)
    start_button.pack(pady=20)

    led_label = ctk.CTkLabel(app, text="", width=20, height=20, bg_color="red")
    led_label.place(x=370, y=10)  # Position the LED in the top right corner

    app.protocol("WM_DELETE_WINDOW", on_closing)  # Properly close the GUI
    ping_server()  # Perform an instant ping when the program starts
    app.mainloop()