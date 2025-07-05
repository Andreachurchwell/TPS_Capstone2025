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


def create_forecast_segmented_button(parent, on_select_callback, theme="dark"):
    """
    Creates a segmented forecast range selector with custom styles.
    Calls on_select_callback(selected_days: int) when a value is picked.
    """
    def handle_select(value):
        day_mapping = {
            "3": 3,
            "5": 5,
            "7": 7,
            "10": 10,
            "16": 16
        }
        selected_days = day_mapping.get(value)
        if selected_days:
            on_select_callback(selected_days)

    if theme == "dark":
        fg_color = "#2E2E2E"
        selected_color = "#FF6F00"
        unselected_color = "#444444"
        selected_text_color = "white"
        unselected_text_color = "#CCCCCC"
    else:
        fg_color = "#F9F6F3"
        selected_color = "#FFA94D"
        unselected_color = "#E6E6E6"
        selected_text_color = "#222222"
        unselected_text_color = "#555555"

    segmented_btn = ctk.CTkSegmentedButton(
        master=parent,
        values=["3", "5", "7", "10", "16"],
        command=handle_select,
        fg_color=fg_color,
        selected_color=selected_color,
        unselected_color=unselected_color,
        corner_radius=10,
        text_color="white"  # ← only text color used
    )
    segmented_btn.set("3")  # Default selection

    return segmented_btn
