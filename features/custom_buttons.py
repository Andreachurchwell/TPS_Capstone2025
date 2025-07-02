import customtkinter as ctk

def create_button(parent, text, command=None, theme="dark", width=120, height=32, font_size=11):
    """
    Creates a styled CTkButton that works for both dark and light themes.
    """
    if theme == "dark":
        fg_color = "#FF6F00"         # Main button color (orange)
        hover_color = "#FFA040"      # Hover orange
        text_color = "white"
        bg_color = "transparent"     # To blend with dark background
    else:
        fg_color = "#FFA94D"         # Lighter orange for light theme
        hover_color = "#FFB866"
        text_color = "#222222"
        bg_color = "#F9F6F3"         # Matches your light theme background

    return ctk.CTkButton(
        master=parent,
        text=text,
        command=command,
        width=width,
        height=height,
        corner_radius=8,
        fg_color=fg_color,
        hover_color=hover_color,
        text_color=text_color,
        font=ctk.CTkFont("Segoe UI", font_size, "bold"),
        border_width=0,
        bg_color=bg_color          # Makes button background blend in clean
    )