import tkinter as tk
from PIL import Image, ImageTk


class ThemeToggle:
    def __init__(self, parent, toggle_callback, current_theme="dark", size=(24, 24)):
        self.parent = parent
        self.toggle_callback = toggle_callback
        self.current_theme = current_theme
        self.size = size
        self.icon = self.load_icon("assets/icons/dark_light_mode.png", size)
        self.button = self.create_button()

    def load_icon(self, path, size=(24, 24)):
        image = Image.open(path)
        image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def create_button(self):
        return tk.Button(
            self.parent,
            image=self.icon,
            command=self.toggle_theme,
            bg="#2E2E2E",
            bd=0,
            activebackground="#444444",
            relief="flat"
        )

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.toggle_callback(self.current_theme)

    def update_style(self, theme_name):
        """ Call this from `apply_theme()` to sync button with the new theme """
        self.current_theme = theme_name
        new_bg = "#F9F6F3" if theme_name == "light" else "#2E2E2E"
        new_active = "#CCCCCC" if theme_name == "light" else "#444444"
        self.button.configure(bg=new_bg, activebackground=new_active)