import tkinter as tk
from tkinter import ttk
import random
import string
import pyperclip
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading

class PasswordGenerator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Password Generator")
        self.window.geometry("450x550")
        self.window.configure(bg="#1e293b")
        self.window.resizable(False, False)
        
        self.current_password = ""
        self.settings = {
            'length': 16,
            'uppercase': True,
            'lowercase': True,
            'numbers': True,
            'symbols': True
        }
        
        self.setup_ui()
        self.generate_password()
        
        # Handle window close to minimize to tray
        self.window.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.window, bg="#3b82f6", height=60)
        header.pack(fill=tk.X, pady=(0, 20))
        header.pack_propagate(False)
        
        title_label = tk.Label(
            header, 
            text="🔑 Password Generator",
            font=("Arial", 18, "bold"),
            bg="#3b82f6",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Main container
        main_frame = tk.Frame(self.window, bg="#1e293b")
        main_frame.pack(padx=30, pady=10, fill=tk.BOTH, expand=True)
        
        # Password display
        password_frame = tk.Frame(main_frame, bg="#0f172a", relief=tk.RAISED, bd=2)
        password_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.password_var = tk.StringVar(value=self.current_password)
        password_display = tk.Entry(
            password_frame,
            textvariable=self.password_var,
            font=("Courier", 14),
            bg="#1e293b",
            fg="white",
            relief=tk.FLAT,
            justify=tk.CENTER,
            state="readonly"
        )
        password_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        copy_btn = tk.Button(
            password_frame,
            text="📋",
            font=("Arial", 16),
            bg="#6366f1",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.copy_password
        )
        copy_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="",
            font=("Arial", 10),
            bg="#1e293b",
            fg="#10b981"
        )
        self.status_label.pack(pady=(0, 10))
        
        # Generate button
        generate_btn = tk.Button(
            main_frame,
            text="🔄 Generate New Password",
            font=("Arial", 12, "bold"),
            bg="#3b82f6",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.generate_password,
            pady=12
        )
        generate_btn.pack(fill=tk.X, pady=(0, 20))
        
        # Settings section
        settings_frame = tk.LabelFrame(
            main_frame,
            text="Settings",
            font=("Arial", 12, "bold"),
            bg="#1e293b",
            fg="white",
            relief=tk.GROOVE,
            bd=2
        )
        settings_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Length slider
        length_frame = tk.Frame(settings_frame, bg="#1e293b")
        length_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.length_label = tk.Label(
            length_frame,
            text=f"Length: {self.settings['length']}",
            font=("Arial", 11),
            bg="#1e293b",
            fg="white"
        )
        self.length_label.pack(anchor=tk.W)
        
        self.length_slider = tk.Scale(
            length_frame,
            from_=8,
            to=32,
            orient=tk.HORIZONTAL,
            bg="#1e293b",
            fg="white",
            troughcolor="#0f172a",
            highlightthickness=0,
            command=self.update_length
        )
        self.length_slider.set(self.settings['length'])
        self.length_slider.pack(fill=tk.X, pady=(5, 0))
        
        # Checkboxes
        checkbox_frame = tk.Frame(settings_frame, bg="#1e293b")
        checkbox_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.check_vars = {}
        options = [
            ('uppercase', 'Uppercase (A-Z)'),
            ('lowercase', 'Lowercase (a-z)'),
            ('numbers', 'Numbers (0-9)'),
            ('symbols', 'Symbols (!@#$...)')
        ]
        
        for key, label in options:
            var = tk.BooleanVar(value=self.settings[key])
            self.check_vars[key] = var
            
            cb = tk.Checkbutton(
                checkbox_frame,
                text=label,
                variable=var,
                font=("Arial", 10),
                bg="#1e293b",
                fg="white",
                selectcolor="#0f172a",
                activebackground="#1e293b",
                activeforeground="white",
                cursor="hand2"
            )
            cb.pack(anchor=tk.W, pady=3)
        
        # Minimize button
        minimize_btn = tk.Button(
            main_frame,
            text="⬇️ Minimize to Tray",
            font=("Arial", 10),
            bg="#475569",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.minimize_to_tray,
            pady=8
        )
        minimize_btn.pack(fill=tk.X)
    
    def generate_password(self):
        # Update settings from checkboxes
        for key, var in self.check_vars.items():
            self.settings[key] = var.get()
        
        chars = ''
        if self.settings['lowercase']:
            chars += string.ascii_lowercase
        if self.settings['uppercase']:
            chars += string.ascii_uppercase
        if self.settings['numbers']:
            chars += string.digits
        if self.settings['symbols']:
            chars += '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
        if not chars:
            chars = string.ascii_lowercase
        
        self.current_password = ''.join(random.choice(chars) for _ in range(self.settings['length']))
        self.password_var.set(self.current_password)
        self.status_label.config(text="")
    
    def copy_password(self):
        if self.current_password:
            pyperclip.copy(self.current_password)
            self.status_label.config(text="✓ Copied to clipboard!")
            self.window.after(2000, lambda: self.status_label.config(text=""))
    
    def update_length(self, value):
        self.settings['length'] = int(float(value))
        self.length_label.config(text=f"Length: {self.settings['length']}")
    
    def create_tray_icon(self):
        # Create a simple icon image
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='#3b82f6')
        dc = ImageDraw.Draw(image)
        dc.rectangle([16, 16, 48, 48], fill='white')
        dc.rectangle([24, 20, 28, 44], fill='#3b82f6')
        dc.rectangle([36, 20, 40, 44], fill='#3b82f6')
        
        menu = Menu(
            MenuItem('Show', self.show_window),
            MenuItem('Copy Latest Password', self.copy_password),
            MenuItem('Generate New', self.generate_new_from_tray),
            MenuItem('Exit', self.quit_app)
        )
        
        self.icon = Icon("password_gen", image, "Password Generator", menu)
    
    def minimize_to_tray(self):
        self.window.withdraw()
        self.create_tray_icon()
        threading.Thread(target=self.icon.run, daemon=True).start()
    
    def show_window(self):
        self.icon.stop()
        self.window.deiconify()
    
    def generate_new_from_tray(self):
        self.generate_password()
        self.copy_password()
    
    def quit_app(self):
        self.icon.stop()
        self.window.quit()
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = PasswordGenerator()
    app.run()