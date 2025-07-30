import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from features.custom_buttons import create_button
plt.rcParams["font.family"] = "Lucida Bright"
plt.rcParams["axes.unicode_minus"] = False
def render_team_dashboard(parent_frame, csv_path="team_7_Folder/team_weather_data.csv", theme="dark", unit="Celsius", show_main_callback=None):
    # Clear existing widgets
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Hide unit toggle if it exists
    if hasattr(parent_frame.master, "unit_toggle"):
        parent_frame.master.unit_toggle.pack_forget()

    # Theme colors
    bg_color = "#1F1F1F" if theme == "dark" else "#F2F2F2"
    text_color = "white" if theme == "dark" else "black"
    parent_frame.configure(fg_color=bg_color)

    # Load and prepare data
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")
    df["month_str"] = df["month"].astype(str)

    cities = df["city"].unique().tolist()
    months = sorted(df["month_str"].unique().tolist())

    city_colors = {
        "Selmer": "#FF8200",
        "Atlanta": "#FFC75F",
        "Bronx": "#0047AB",
        "Oxnard": "#FF6F61",
        "Clearwater": "#2AA5A0",
        "Queens": "#A569BD"
    }

    # Layout frames
    top_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    top_frame.pack(pady=10, fill="x")

    chart_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    chart_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # Dropdown variables
    chart_options = [
        "Monthly Avg Min/Max Temp",
        "Total Monthly Precipitation",
        "Max Wind Speed by Month"
    ]
    selected_chart = ctk.StringVar(value=chart_options[0])
    selected_city = ctk.StringVar(value="All")
    selected_month = ctk.StringVar(value="All")

    # Styled dropdown colors
    menu_fg = "#3A3A3A"
    menu_text = "white"
    menu_button = "#FF8200"
    menu_dropdown_fg = "#2B2B2B"
    menu_dropdown_text = "white"
    menu_hover = "#FF9A3C"

    # Dropdowns
    chart_menu = ctk.CTkOptionMenu(
        top_frame, values=chart_options, variable=selected_chart,
        command=lambda _: draw_chart(),
        fg_color=menu_fg, button_color=menu_button, text_color=menu_text,
        dropdown_fg_color=menu_dropdown_fg, dropdown_text_color=menu_dropdown_text,
        dropdown_hover_color=menu_hover,
        font=ctk.CTkFont("Lucida Bright", 12) 
    )
    chart_menu.pack(side="left", padx=10)

    city_menu = ctk.CTkOptionMenu(
        top_frame, values=["All"] + cities, variable=selected_city,
        command=lambda _: draw_chart(),
        fg_color=menu_fg, button_color=menu_button, text_color=menu_text,
        dropdown_fg_color=menu_dropdown_fg, dropdown_text_color=menu_dropdown_text,
        dropdown_hover_color=menu_hover,
        font=ctk.CTkFont("Lucida Bright", 12) 
        
    )
    city_menu.pack(side="left", padx=10)

    month_menu = ctk.CTkOptionMenu(
        top_frame, values=["All"] + months, variable=selected_month,
        command=lambda _: draw_chart(),
        fg_color=menu_fg, button_color=menu_button, text_color=menu_text,
        dropdown_fg_color=menu_dropdown_fg, dropdown_text_color=menu_dropdown_text,
        dropdown_hover_color=menu_hover,
        font=ctk.CTkFont("Lucida Bright", 12) 
    )
    month_menu.pack(side="left", padx=10)

    # Temp conversion
    def to_fahrenheit(c):
        return c * 9 / 5 + 32

    # Chart rendering function
    def draw_chart():
        for widget in chart_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 4.5))
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        ax.tick_params(axis='x', rotation=45)
        ax.tick_params(colors=text_color)

        # Filters
        city_filter = selected_city.get()
        month_filter = selected_month.get()
        use_fahrenheit = unit == "Fahrenheit"

        filtered_df = df.copy()
        if city_filter != "All":
            filtered_df = filtered_df[filtered_df["city"] == city_filter]
        if month_filter != "All":
            filtered_df = filtered_df[filtered_df["month_str"] == month_filter]

        option = selected_chart.get()

        if option == "Monthly Avg Min/Max Temp":
            plot_cities = [city_filter] if city_filter != "All" else cities
            for city in plot_cities:
                city_data = filtered_df[filtered_df["city"] == city]
                monthly = city_data.groupby("month_str")[["min_temp", "max_temp"]].mean().reset_index()
                if use_fahrenheit:
                    monthly["min_temp"] = monthly["min_temp"].apply(to_fahrenheit)
                    monthly["max_temp"] = monthly["max_temp"].apply(to_fahrenheit)
                ax.plot(monthly["month_str"], monthly["min_temp"], marker="o", label=f"{city} Min", color=city_colors.get(city, "gray"))
                ax.plot(monthly["month_str"], monthly["max_temp"], marker="o", linestyle="--", label=f"{city} Max", color=city_colors.get(city, "gray"))
            ax.set_title("Monthly Avg Min/Max Temp", color=text_color,fontsize=12,fontweight="bold")
            ax.set_ylabel("°F" if use_fahrenheit else "°C",fontsize=10)

        elif option == "Total Monthly Precipitation":
            plot_cities = [city_filter] if city_filter != "All" else cities
            for city in plot_cities:
                city_data = filtered_df[filtered_df["city"] == city]
                monthly = city_data.groupby("month_str")["precip"].sum().reset_index()
                ax.plot(monthly["month_str"], monthly["precip"], marker="s", label=city, color=city_colors.get(city, "gray"))
            ax.set_title("Total Monthly Precipitation", color=text_color,fontsize=12,fontweight="bold")
            ax.set_ylabel("Precipitation (mm or inch)",fontsize=10)

        elif option == "Max Wind Speed by Month":
            plot_cities = [city_filter] if city_filter != "All" else cities
            for city in plot_cities:
                city_data = filtered_df[filtered_df["city"] == city]
                monthly = city_data.groupby("month_str")["max_wind_spd"].max().reset_index()
                ax.plot(monthly["month_str"], monthly["max_wind_spd"], marker="x", label=city, color=city_colors.get(city, "gray"))
            ax.set_title("Max Wind Speed by Month", color=text_color, fontsize=12, fontweight="bold")
            ax.set_ylabel("Max Wind Speed",fontsize=10)

        ax.legend(loc="upper left",  prop={"family": "Lucida Bright", "size": 9})

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    draw_chart()

    # Back button
    back_btn = create_button(
        parent_frame,
        text="← Back to Home",
        command=lambda: show_main_callback() if show_main_callback else None
    )
    back_btn.pack(pady=20)

