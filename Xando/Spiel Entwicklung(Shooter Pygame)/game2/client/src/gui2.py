import customtkinter
import os
import threading
import time
from PIL import Image  # Package name is Pillow!!!
from game import start_game  # Import the start_game function
import socket
# disable gui while ingame(maybe with variable from Spielfeld.py that you check here.
# error: crash on start button when server online

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Voidshot Launcher")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with dark mode image only
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets/icons/gui")
        self.home_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "home.png")), size=(20, 20))

        # Sidebar Section
        # ------------------------------
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="VoidShot",
                                                             compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color="gray90", hover_color="gray30",
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                                      fg_color="transparent", text_color="gray90", hover_color="gray30",
                                                      anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Account",
                                                      fg_color="transparent", text_color="gray90", hover_color="gray30",
                                                      anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.offline_checkbox = customtkinter.CTkCheckBox(self.navigation_frame, text="Offline", command=self.dummy_function)
        self.offline_checkbox.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="s")

        self.quit_button = customtkinter.CTkButton(self.navigation_frame, text="Quit", command=self.quit)
        self.quit_button.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        # ------------------------------

        # Home Frame Section
        # ------------------------------
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.start_game_button = customtkinter.CTkButton(self.home_frame, text="Start Game", command=self.start_game_1, state="disabled")
        self.start_game_button.grid(row=0, column=0, padx=20, pady=10)

        self.server_status_led = customtkinter.CTkLabel(self.home_frame, text="●", text_color="red", font=customtkinter.CTkFont(size=20))
        self.server_status_led.grid(row=1, column=0, padx=20, pady=10)
        # ------------------------------

        # Second Frame Section
        # ------------------------------
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # ------------------------------

        # Third Frame Section
        # ------------------------------
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # ------------------------------

        # select default frame
        self.select_frame_by_name("home")

        # Start server status check
        self.check_server_status()

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color="gray25" if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color="gray25" if name == "settings" else "transparent")
        self.frame_3_button.configure(fg_color="gray25" if name == "account" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "settings":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "account":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("settings")

    def frame_3_button_event(self):
        self.select_frame_by_name("account")

    def dummy_function(self):
        print("Offline checkbox toggled")

    def start_game_1(self):
        start_game()  # Call the start_game function from Spielfeld.py

    def disable_buttons(self):
        for widget in self.winfo_children():
            if isinstance(widget, customtkinter.CTkButton):
                widget.configure(state="disabled")

    def enable_buttons(self):
        for widget in self.winfo_children():
            if isinstance(widget, customtkinter.CTkButton):
                widget.configure(state="normal")

    def check_server_status(self):
        def ping_server():
            while True:
                try:
                    # Replace 'localhost' and 52983 with your server's address and port
                    with socket.create_connection(("localhost", 52983), timeout=5):
                        self.server_status_led.configure(text_color="green")
                        self.start_game_button.configure(state="normal")
                except OSError:
                    self.server_status_led.configure(text_color="red")
                    self.start_game_button.configure(state="disabled")
                time.sleep(10)

        threading.Thread(target=ping_server, daemon=True).start()

if __name__ == "__main__":
    app = App()
    app.mainloop()