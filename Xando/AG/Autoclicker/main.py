import customtkinter as ctk
import pyautogui
import keyboard
import threading
import time
from typing import Optional

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("red.json")  # Changed from "dark-red" to "blue" (a valid default theme)

class AutoClickerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Main window configuration
        self.title("Advanced AutoClicker")
        self.geometry("500x650")
        self.resizable(False, False)

        # Variables
        self.clicking = False
        self.click_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        
        # Click settings
        self.click_interval = ctk.DoubleVar(value=1.0)
        self.click_counter = ctk.IntVar(value=0)
        self.click_limit = ctk.IntVar(value=0)  # 0 means unlimited
        self.click_type = ctk.StringVar(value="left")
        self.position_type = ctk.StringVar(value="current")
        self.x_position = ctk.IntVar(value=0)
        self.y_position = ctk.IntVar(value=0)
        self.hotkey = ctk.StringVar(value="f6")

        # Create UI
        self.create_ui()

        # Setup hotkey
        keyboard.add_hotkey(self.hotkey.get(), self.toggle_clicking)

        # Protocol for closing the app
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="ADVANCED AUTOCLICKER", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))

        # Click interval frame
        interval_frame = ctk.CTkFrame(main_frame)
        interval_frame.pack(fill="x", padx=10, pady=10)

        interval_label = ctk.CTkLabel(
            interval_frame, 
            text="Click Interval (seconds)", 
            font=ctk.CTkFont(size=16)
        )
        interval_label.pack(anchor="w", padx=10, pady=(10, 0))

        interval_slider = ctk.CTkSlider(
            interval_frame,
            from_=0.01,
            to=5.0,
            variable=self.click_interval,
            number_of_steps=499
        )
        interval_slider.pack(fill="x", padx=10, pady=5)

        interval_entry = ctk.CTkEntry(interval_frame)
        interval_entry.pack(fill="x", padx=10, pady=5)
        interval_entry.insert(0, f"{self.click_interval.get():.2f}")

        # Update entry when slider changes
        def update_entry(_):
            interval_entry.delete(0, "end")
            interval_entry.insert(0, f"{self.click_interval.get():.2f}")
        
        # Update slider when entry changes
        def update_slider(_=None):
            try:
                value = float(interval_entry.get())
                if 0.01 <= value <= 5.0:
                    self.click_interval.set(value)
            except ValueError:
                interval_entry.delete(0, "end")
                interval_entry.insert(0, f"{self.click_interval.get():.2f}")

        interval_slider.configure(command=update_entry)
        interval_entry.bind("<FocusOut>", update_slider)
        interval_entry.bind("<Return>", update_slider)

        # Click options frame
        click_options_frame = ctk.CTkFrame(main_frame)
        click_options_frame.pack(fill="x", padx=10, pady=10)

        click_options_label = ctk.CTkLabel(
            click_options_frame, 
            text="Click Options", 
            font=ctk.CTkFont(size=16)
        )
        click_options_label.pack(anchor="w", padx=10, pady=(10, 0))

        # Click type selection
        click_type_frame = ctk.CTkFrame(click_options_frame, fg_color="transparent")
        click_type_frame.pack(fill="x", padx=10, pady=5)

        click_type_label = ctk.CTkLabel(click_type_frame, text="Mouse Button:")
        click_type_label.pack(side="left", padx=(0, 10))

        left_radio = ctk.CTkRadioButton(
            click_type_frame, 
            text="Left", 
            variable=self.click_type, 
            value="left"
        )
        left_radio.pack(side="left", padx=(0, 10))

        right_radio = ctk.CTkRadioButton(
            click_type_frame, 
            text="Right", 
            variable=self.click_type, 
            value="right"
        )
        right_radio.pack(side="left", padx=(0, 10))

        middle_radio = ctk.CTkRadioButton(
            click_type_frame, 
            text="Middle", 
            variable=self.click_type, 
            value="middle"
        )
        middle_radio.pack(side="left", padx=(0, 10))

        # Click limit
        click_limit_frame = ctk.CTkFrame(click_options_frame, fg_color="transparent")
        click_limit_frame.pack(fill="x", padx=10, pady=5)

        click_limit_checkbox_var = ctk.BooleanVar(value=False)
        click_limit_checkbox = ctk.CTkCheckBox(
            click_limit_frame,
            text="Limit clicks",
            variable=click_limit_checkbox_var
        )
        click_limit_checkbox.pack(side="left", padx=(0, 10))

        click_limit_entry = ctk.CTkEntry(
            click_limit_frame, 
            width=100, 
            state="disabled"
        )
        click_limit_entry.pack(side="left", padx=(0, 5))
        click_limit_entry.insert(0, "0")

        def toggle_limit():
            if click_limit_checkbox_var.get():
                click_limit_entry.configure(state="normal")
                try:
                    self.click_limit.set(int(click_limit_entry.get()))
                except ValueError:
                    click_limit_entry.delete(0, "end")
                    click_limit_entry.insert(0, "100")
                    self.click_limit.set(100)
            else:
                click_limit_entry.configure(state="disabled")
                self.click_limit.set(0)

        click_limit_checkbox.configure(command=toggle_limit)

        # Position options frame
        position_frame = ctk.CTkFrame(main_frame)
        position_frame.pack(fill="x", padx=10, pady=10)

        position_label = ctk.CTkLabel(
            position_frame, 
            text="Click Position", 
            font=ctk.CTkFont(size=16)
        )
        position_label.pack(anchor="w", padx=10, pady=(10, 0))

        # Position type selection
        position_type_frame = ctk.CTkFrame(position_frame, fg_color="transparent")
        position_type_frame.pack(fill="x", padx=10, pady=5)

        current_pos_radio = ctk.CTkRadioButton(
            position_type_frame, 
            text="Current Mouse Position", 
            variable=self.position_type, 
            value="current"
        )
        current_pos_radio.pack(anchor="w", padx=5, pady=2)

        custom_pos_radio = ctk.CTkRadioButton(
            position_type_frame, 
            text="Custom Position", 
            variable=self.position_type, 
            value="custom"
        )
        custom_pos_radio.pack(anchor="w", padx=5, pady=2)

        # Custom position coordinates
        custom_pos_frame = ctk.CTkFrame(position_frame, fg_color="transparent")
        custom_pos_frame.pack(fill="x", padx=10, pady=5)

        x_label = ctk.CTkLabel(custom_pos_frame, text="X:")
        x_label.pack(side="left", padx=(0, 5))

        x_entry = ctk.CTkEntry(custom_pos_frame, width=70)
        x_entry.pack(side="left", padx=(0, 10))
        x_entry.insert(0, "0")

        y_label = ctk.CTkLabel(custom_pos_frame, text="Y:")
        y_label.pack(side="left", padx=(0, 5))

        y_entry = ctk.CTkEntry(custom_pos_frame, width=70)
        y_entry.pack(side="left", padx=(0, 10))
        y_entry.insert(0, "0")

        get_pos_button = ctk.CTkButton(
            custom_pos_frame, 
            text="Get Current", 
            width=100,
            command=self.get_current_position
        )
        get_pos_button.pack(side="left", padx=(0, 10))

        def update_position_entries():
            if self.position_type.get() == "custom":
                try:
                    self.x_position.set(int(x_entry.get()))
                    self.y_position.set(int(y_entry.get()))
                except ValueError:
                    x, y = pyautogui.position()
                    x_entry.delete(0, "end")
                    x_entry.insert(0, str(x))
                    y_entry.delete(0, "end")
                    y_entry.insert(0, str(y))
                    self.x_position.set(x)
                    self.y_position.set(y)

        # Set the update function to both radio buttons
        current_pos_radio.configure(command=update_position_entries)
        custom_pos_radio.configure(command=update_position_entries)

        # Hotkey frame
        hotkey_frame = ctk.CTkFrame(main_frame)
        hotkey_frame.pack(fill="x", padx=10, pady=10)

        hotkey_label = ctk.CTkLabel(
            hotkey_frame, 
            text="Hotkey Settings", 
            font=ctk.CTkFont(size=16)
        )
        hotkey_label.pack(anchor="w", padx=10, pady=(10, 0))

        hotkey_input_frame = ctk.CTkFrame(hotkey_frame, fg_color="transparent")
        hotkey_input_frame.pack(fill="x", padx=10, pady=5)

        hotkey_entry_label = ctk.CTkLabel(hotkey_input_frame, text="Toggle Hotkey:")
        hotkey_entry_label.pack(side="left", padx=(0, 10))

        hotkey_entry = ctk.CTkEntry(hotkey_input_frame, width=100)
        hotkey_entry.pack(side="left", padx=(0, 5))
        hotkey_entry.insert(0, self.hotkey.get())

        hotkey_apply = ctk.CTkButton(
            hotkey_input_frame, 
            text="Apply", 
            width=80,
            command=lambda: self.set_hotkey(hotkey_entry.get())
        )
        hotkey_apply.pack(side="left", padx=(0, 10))

        # Status and control frame
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="x", padx=10, pady=10)

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Status: Idle",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.status_label.pack(pady=10)

        self.counter_label = ctk.CTkLabel(
            status_frame,
            text="Clicks: 0",
            font=ctk.CTkFont(size=14)
        )
        self.counter_label.pack(pady=5)

        button_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=10)

        start_button = ctk.CTkButton(
            button_frame,
            text="Start (F6)",
            command=self.start_clicking,
            fg_color="#8B0000",  # Dark red
            hover_color="#5C0000",  # Darker red
            width=120
        )
        start_button.pack(side="left", padx=10, expand=True)

        stop_button = ctk.CTkButton(
            button_frame,
            text="Stop (F6)",
            command=self.stop_clicking,
            fg_color="#333333",  # Dark gray
            hover_color="#1A1A1A",  # Darker gray
            width=120
        )
        stop_button.pack(side="right", padx=10, expand=True)

    def get_current_position(self):
        # Wait a bit to allow user to position mouse
        self.after(1000, self._get_position)

    def _get_position(self):
        x, y = pyautogui.position()
        # Update the coordinate entries
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                self._find_and_update_entries(widget, x, y)
        self.x_position.set(x)
        self.y_position.set(y)
    
    def _find_and_update_entries(self, parent, x, y):
        for child in parent.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                self._find_and_update_entries(child, x, y)
            elif isinstance(child, ctk.CTkEntry) and child.winfo_width() == 70:
                # If this is the x entry (first of the two we encounter)
                if not hasattr(self, "_found_x_entry"):
                    child.delete(0, "end")
                    child.insert(0, str(x))
                    self._found_x_entry = True
                else:
                    child.delete(0, "end")
                    child.insert(0, str(y))
                    self._found_x_entry = False

    def toggle_clicking(self):
        if self.clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

    def set_hotkey(self, key):
        # Remove old hotkey
        try:
            keyboard.remove_hotkey(self.hotkey.get())
        except:
            pass
        
        # Set new hotkey
        self.hotkey.set(key)
        keyboard.add_hotkey(key, self.toggle_clicking)

    def start_clicking(self):
        if not self.clicking:
            self.clicking = True
            self.stop_event.clear()
            self.click_counter.set(0)
            self.status_label.configure(text="Status: Running", text_color="#FF0000")  # Bright red
            self.click_thread = threading.Thread(target=self.clicking_thread)
            self.click_thread.daemon = True
            self.click_thread.start()

    def stop_clicking(self):
        if self.clicking:
            self.clicking = False
            self.stop_event.set()
            self.status_label.configure(text="Status: Stopped", text_color="#FFFFFF")  # White
            if self.click_thread:
                self.click_thread.join(timeout=1.0)
                self.click_thread = None

    def clicking_thread(self):
        limit = self.click_limit.get()
        count = 0
        
        while self.clicking and (limit == 0 or count < limit):
            # Check if we should stop
            if self.stop_event.is_set():
                break
                
            # Handle position
            current_pos = pyautogui.position()
            if self.position_type.get() == "custom":
                x, y = self.x_position.get(), self.y_position.get()
                pyautogui.moveTo(x, y)
            
            # Perform click based on selected type
            click_type = self.click_type.get()
            if click_type == "left":
                pyautogui.click()
            elif click_type == "right":
                pyautogui.rightClick()
            elif click_type == "middle":
                pyautogui.middleClick()
            
            # Move back to original position if using custom position
            if self.position_type.get() == "custom":
                pyautogui.moveTo(current_pos)
                
            # Update counter
            count += 1
            self.click_counter.set(count)
            self.counter_label.configure(text=f"Clicks: {count}")
            
            # Wait for the specified interval
            try:
                time.sleep(self.click_interval.get())
            except (ValueError, TypeError):
                time.sleep(1.0)
        
        # Update status based on stopping condition
        if limit > 0 and count >= limit:
            self.clicking = False
            self.after(0, lambda: self.status_label.configure(text="Status: Finished", text_color="#00FF00"))
        elif self.stop_event.is_set():
            self.after(0, lambda: self.status_label.configure(text="Status: Stopped", text_color="#FFFFFF"))

    def on_close(self):
        self.stop_clicking()
        try:
            keyboard.remove_hotkey(self.hotkey.get())
        except:
            pass
        self.destroy()

if __name__ == "__main__":
    app = AutoClickerApp()
    
    # Set custom theme with red and black colors
    app.configure(fg_color="#1A1A1A")  # Dark background for main window
    
    # Override default CTk colors for red and black theme
    ctk.ThemeManager.theme["CTkFrame"]["fg_color"] = ["#2A2A2A", "#2A2A2A"]
    ctk.ThemeManager.theme["CTkButton"]["fg_color"] = ["#8B0000", "#8B0000"]  # Dark red
    ctk.ThemeManager.theme["CTkButton"]["hover_color"] = ["#5C0000", "#5C0000"]  # Darker red
    ctk.ThemeManager.theme["CTkCheckBox"]["fg_color"] = ["#8B0000", "#8B0000"]  # Dark red
    ctk.ThemeManager.theme["CTkRadioButton"]["fg_color"] = ["#8B0000", "#8B0000"]  # Dark red
    ctk.ThemeManager.theme["CTkSlider"]["button_color"] = ["#B22222", "#B22222"]  # Brighter red
    ctk.ThemeManager.theme["CTkSlider"]["button_hover_color"] = ["#FF0000", "#FF0000"]  # Brightest red
    ctk.ThemeManager.theme["CTkSlider"]["progress_color"] = ["#8B0000", "#8B0000"]  # Dark red
    
    app.mainloop()
