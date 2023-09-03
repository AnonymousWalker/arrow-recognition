import tkinter as tk
import time
import sys
import keyboard
from src.config import Config
from application import AutoApp

class ConfigGUI:
    def __init__(self, root, console: AutoApp, config: Config):
        self.root = root
        self.root.title("Config GUI")
        self.config = config
        self.app_console = console
        self.is_editing = False
        self.focus_loss_timer = None

        # Create and configure frames for input groups
        self.key_typing_sleep_frame = tk.Frame(root)
        self.key_typing_sleep_frame.pack(fill=tk.X, padx=10, pady=5)

        self.current_level_frame = tk.Frame(root)
        self.current_level_frame.pack(fill=tk.X, padx=10, pady=5)

        self.speed_frame = tk.Frame(root)
        self.speed_frame.pack(fill=tk.X, padx=10, pady=5)

        # Create and configure GUI elements for KEY_TYPING_SLEEP
        self.key_typing_sleep_label = tk.Label(self.key_typing_sleep_frame, text="Thoi gian bam:")
        self.key_typing_sleep_label.pack(side=tk.LEFT)

        self.increase_key_typing_sleep_button = tk.Button(self.key_typing_sleep_frame, text="+", command=self.increase_key_typing_sleep, padx=5)
        self.increase_key_typing_sleep_button.pack(side=tk.RIGHT)

        self.key_typing_sleep_entry = tk.Entry(self.key_typing_sleep_frame, font=("Arial", 12), width=7)
        self.key_typing_sleep_entry.insert(0, str(self.config.KEY_TYPING_SLEEP))
        self.key_typing_sleep_entry.pack(side=tk.RIGHT)


        self.decrease_key_typing_sleep_button = tk.Button(self.key_typing_sleep_frame, text="-", command=self.decrease_key_typing_sleep, padx=5)
        self.decrease_key_typing_sleep_button.pack(side=tk.RIGHT)

        # Create and configure GUI elements for CURRENT_LEVEL
        self.current_level_label = tk.Label(self.current_level_frame, text="Level:")
        self.current_level_label.pack(side=tk.LEFT)

        self.increase_level_button = tk.Button(self.current_level_frame, text="+", command=self.increase_level, padx=5)
        self.increase_level_button.pack(side=tk.RIGHT)

        self.current_level_entry = tk.Entry(self.current_level_frame, font=("Arial", 12), width=7)
        self.current_level_entry.insert(0, str(self.config.CURRENT_LEVEL))
        self.current_level_entry.pack(side=tk.RIGHT)


        self.decrease_level_button = tk.Button(self.current_level_frame, text="-", command=self.decrease_level, padx=5)
        self.decrease_level_button.pack(side=tk.RIGHT)

        # Create and configure GUI elements for Speed
        self.speed_label = tk.Label(self.speed_frame, text="Speed:")
        self.speed_label.pack(side=tk.LEFT)

        self.increase_speed_button = tk.Button(self.speed_frame, text="+", command=self.increase_speed, padx=5)
        self.increase_speed_button.pack(side=tk.RIGHT)

        self.speed_entry = tk.Entry(self.speed_frame, font=("Arial", 12), width=7)
        self.speed_entry.insert(0, str(self.config.speed))
        self.speed_entry.pack(side=tk.RIGHT)


        self.decrease_speed_button = tk.Button(self.speed_frame, text="-", command=self.decrease_speed, padx=5)
        self.decrease_speed_button.pack(side=tk.RIGHT)

        self.save_button = tk.Button(root, text="OK", command=self.save_config)
        self.save_button.pack()

        self.root.columnconfigure(2, weight=0)

        # Register the key listener
        keyboard.on_press(self.key_listener)
        
        self.root.bind("<FocusIn>", self.on_focus_in)
        self.root.bind("<FocusOut>", self.on_focus_out)

    def key_listener(self, e):
        if e.event_type == keyboard.KEY_DOWN:
            if e.name == 'page up':
                self.increase_speed()
            if e.name == 'page down':
                self.decrease_speed()
            if e.name == 'f11':
                self.increase_level()
            if e.name == 'f10':
                self.decrease_level()
            if e.name =='`':
                sys.exit(0)

    def increase_speed(self):
        self.config.speed += self.config.ADJUST_SPEED_AMOUNT
        self.speed_entry.delete(0, tk.END)
        self.speed_entry.insert(0, str(self.config.speed))
        print('speed: {}'.format(self.config.speed))

    def decrease_speed(self):
        self.config.speed -= self.config.ADJUST_SPEED_AMOUNT
        self.speed_entry.delete(0, tk.END)
        self.speed_entry.insert(0, str(self.config.speed))
        print('speed: {}'.format(self.config.speed))

    def increase_level(self):
        self.config.CURRENT_LEVEL += 1
        self.current_level_entry.delete(0, tk.END)
        self.current_level_entry.insert(0, str(self.config.CURRENT_LEVEL))
        print(f"Level: {self.config.CURRENT_LEVEL}")

    def decrease_level(self):
        self.config.CURRENT_LEVEL -= 1
        self.current_level_entry.delete(0, tk.END)
        self.current_level_entry.insert(0, str(self.config.CURRENT_LEVEL))
        print(f"Level: {self.config.CURRENT_LEVEL}")

    def increase_key_typing_sleep(self):
        self.config.KEY_TYPING_SLEEP = round(self.config.KEY_TYPING_SLEEP + 0.01, 2)
        self.key_typing_sleep_entry.delete(0, tk.END)
        self.key_typing_sleep_entry.insert(0, str(self.config.KEY_TYPING_SLEEP))
        print('Typing speed: {}'.format(self.config.KEY_TYPING_SLEEP))

    def decrease_key_typing_sleep(self):
        self.config.KEY_TYPING_SLEEP = round(self.config.KEY_TYPING_SLEEP - 0.01, 2)
        self.key_typing_sleep_entry.delete(0, tk.END)
        self.key_typing_sleep_entry.insert(0, str(self.config.KEY_TYPING_SLEEP))
        print('Typing speed: {}'.format(self.config.KEY_TYPING_SLEEP))

    def save_config(self):
        # Update the config values based on the GUI input
        self.config.KEY_TYPING_SLEEP = float(self.key_typing_sleep_entry.get())
        self.config.CURRENT_LEVEL = int(self.current_level_entry.get())
        self.config.speed = float(self.speed_entry.get())
        
        self.app_console.set_focus(True)
        self.is_editing = False


    def on_focus_in(self, event):
        self.is_editing = True
        self.app_console.set_focus(False)

        if self.focus_loss_timer:
            # Cancel the focus loss event if focus returns to the window
            self.root.after_cancel(self.focus_loss_timer)
            self.focus_loss_timer = None

    def on_focus_out(self, event):
        # Check if the time since the last focus event is very short (e.g., a click within the window)
        if not self.focus_loss_timer:
            self.focus_loss_timer = self.root.after(10, self.handle_focus_loss)
            return

    def handle_focus_loss(self):
        if self.is_editing:
            self.save_button.focus_set()

        

if __name__ == "__main__":
    root = tk.Tk()
    config = Config()
    console = AutoApp(config)
    app = ConfigGUI(root, console, config)
    console.run()
    root.mainloop()
