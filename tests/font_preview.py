# import customtkinter as ctk
# import tkinter.font as tkfont

# # Initialize app
# ctk.set_appearance_mode("dark")
# app = ctk.CTk()
# app.title("Font Preview")
# app.geometry("400x600")

# # Sample fonts to try — feel free to add or remove
# font_list = [
#     "Arial", "Helvetica", "Segoe UI", "Calibri", "Comic Sans MS", "Courier New",
#     "Georgia", "Impact", "Lucida Console", "Lucida Sans", "Tahoma",
#     "Times New Roman", "Trebuchet MS", "Verdana", "Futura", "Roboto", 
#     "Bebas Neue", "Montserrat", "Orbitron", "Raleway", "Oswald"
# ]

# # Scrollable frame
# scrollable = ctk.CTkScrollableFrame(app, width=380, height=580)
# scrollable.pack(pady=10)

# # Add a label for each font
# for font_name in font_list:
#     try:
#         preview_font = (font_name, 16, "bold")
#         label = ctk.CTkLabel(scrollable, text=font_name, font=preview_font)
#         label.pack(pady=5)
#     except tkfont.TclError:
#         # Font not found on the system
#         label = ctk.CTkLabel(scrollable, text=f"{font_name} (Not Found)", font=("Arial", 12, "italic"), text_color="gray")
#         label.pack(pady=5)

# app.mainloop()


import customtkinter as ctk
import tkinter as tk
import tkinter.font as tkfont

# Setup
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("All Fonts Preview")
app.geometry("500x700")

# Get all fonts installed on your system
root = tk.Tk()
root.withdraw()  # hide default Tk window
all_fonts = sorted(set(tkfont.families()))

# Scrollable frame
scrollable = ctk.CTkScrollableFrame(app, width=480, height=680)
scrollable.pack(padx=10, pady=10)

# Show sample text in each font
sample_text = "Volunteer Weather 🌤️"

for font_name in all_fonts:
    try:
        label = ctk.CTkLabel(scrollable, text=f"{font_name}: {sample_text}", font=(font_name, 16, "bold"))
        label.pack(pady=4)
    except tk.TclError:
        # Skip fonts that aren't usable
        continue

app.mainloop()