import tkinter as tk
from core.geocoding import get_city_suggestions
import threading

class AutocompleteEntry(tk.Frame):  # Subclass Frame, not Entry
    def __init__(self, master=None, theme_colors=None, **kwargs):
        super().__init__(master)

        self.theme_colors = theme_colors or {
            "bg": "#FFFFFF",
            "fg": "#000000",
            "highlight": "#FFA94D",
            "border": "#999999"
        }

        # Create the inner Entry widget (styled)
        self.entry = tk.Entry(
            self,
            bd=0,
            relief=tk.FLAT,
            highlightthickness=0,
            bg=self.theme_colors["bg"],
            fg=self.theme_colors["fg"],
            insertbackground=self.theme_colors["fg"],
            font=kwargs.get("font", ("Segoe UI", 12))
        )
        self.entry.pack(fill="both", expand=True, padx=4, pady=4)

        # Optional: outer frame border simulation
        self.configure(
            bg=self.theme_colors["border"],
            padx=1,
            pady=1
        )

        # Autocomplete behavior
        self.popup = None
        self.after_id = None
        self.last_query = ""
        self.selected_location = None

        self.entry.bind("<KeyRelease>", self.delayed_fetch)
        self.entry.bind("<Down>", self.move_down)

    def get(self):
        return self.entry.get()

    def delete(self, start, end):
        self.entry.delete(start, end)

    def insert(self, index, value):
        self.entry.insert(index, value)

    def delayed_fetch(self, event=None):
        if self.after_id:
            self.after_cancel(self.after_id)

        # Capitalize first letter
        current_text = self.entry.get()
        if current_text:
            capitalized = current_text[0].upper() + current_text[1:]
            self.entry.delete(0, tk.END)
            self.entry.insert(0, capitalized)

        self.after_id = self.after(300, self.start_thread)

    def start_thread(self):
        threading.Thread(target=self.update_suggestions, daemon=True).start()

    def update_suggestions(self):
        typed = self.get().strip()
        if typed == self.last_query:
            return

        self.last_query = typed

        if not typed:
            self.after(0, self.hide_popup)
            return

        matches = get_city_suggestions(typed)
        if matches:
            self.after(0, lambda: self.show_popup(matches))
        else:
            self.after(0, self.hide_popup)

    def show_popup(self, matches):
        self.hide_popup()
        self.current_suggestions = matches

        self.popup = tk.Toplevel(self)
        self.popup.wm_overrideredirect(True)
        self.popup.wm_geometry(self.popup_position())

        self.listbox = tk.Listbox(
            self.popup,
            width=self.entry["width"],
            height=min(len(matches), 6),
            bg=self.theme_colors["bg"],
            fg=self.theme_colors["fg"],
            selectbackground=self.theme_colors["highlight"],
            selectforeground="white",
            relief=tk.FLAT,
            borderwidth=1
        )
        self.listbox.pack()
        self.listbox.bind("<<ListboxSelect>>", self.select_city)

        for match in matches:
            self.listbox.insert(tk.END, match["label"])
    def popup_position(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        return f"+{x}+{y}"
    

    def select_city(self, event=None):
        if not self.popup or not hasattr(self, "current_suggestions"):
            return

        index = self.listbox.curselection()
        if not index:
            return

        selected_index = index[0]
        selected_item = self.current_suggestions[selected_index]

        # Fill the entry with just the label
        self.entry.delete(0, tk.END)
        self.entry.insert(0, selected_item["label"])

        # Store the selected location with lat/lon
        self.selected_location = {
            "lat": selected_item["lat"],
            "lon": selected_item["lon"],
            "label": selected_item["label"]
        }
        # print("[DEBUG] Selected Location:", self.selected_location)
        self.hide_popup()

    def move_down(self, event):
        if self.popup:
            listbox = self.popup.winfo_children()[0]
            listbox.focus_set()
            listbox.selection_set(0)

    def hide_popup(self):
        if self.popup:
            self.popup.destroy()
            self.popup = None
