import tkinter as tk
from tkinter import ttk
import threading
import time
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, Key

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")
        self.root.geometry("300x200")
        
        self.running = False
        self.cps = tk.DoubleVar(value=10)
        self.mouse = Controller()
        
        ttk.Label(root, text="CPS (Clicks Per Second):").pack(pady=5)
        self.cps_entry = ttk.Entry(root, textvariable=self.cps)
        self.cps_entry.pack(pady=5)
        
        self.status_label = ttk.Label(root, text="Status: Stopped", foreground="red")
        self.status_label.pack(pady=5)
        
        self.listener_thread = threading.Thread(target=self.keyboard_listener, daemon=True)
        self.listener_thread.start()
    
    def click_loop(self):
        while self.running:
            delay = 1 / max(self.cps.get(), 1)
            self.mouse.click(Button.left)
            time.sleep(delay)
    
    def toggle_clicking(self):
        if self.running:
            self.running = False
            self.status_label.config(text="Status: Stopped", foreground="red")
        else:
            self.running = True
            self.status_label.config(text="Status: Running", foreground="green")
            threading.Thread(target=self.click_loop, daemon=True).start()
    
    def keyboard_listener(self):
        def on_press(key):
            if key == Key.tab:
                self.toggle_clicking()
        
        with Listener(on_press=on_press) as listener:
            listener.join()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
