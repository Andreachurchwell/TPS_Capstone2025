import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from features.custom_buttons import create_button  # make sure this import is in your file

def render_team_dashboard(parent_frame, csv_path="team_7_Folder/team_weather_data.csv", theme="dark", show_main_callback=None):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    bg_color = "#1F1F1F" if theme == "dark" else "#F2F2F2"
    text_color = "white" if theme == "dark" else "black"
    parent_frame.configure(fg_color=bg_color)

    # Load and prep data
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
        "Oxnard": "#FF6F61"
    }

    # Top UI area (dropdowns + toggles)
    top_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    top_frame.pack(pady=10, fill="x")

    # Chart container frame
    chart_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    chart_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # Dropdown state variables
    chart_options = [
        "Monthly Avg Min/Max Temp",
        "Total Monthly Precipitation",
        "Max Wind Speed by Month"
    ]
    selected_chart = ctk.StringVar(value=chart_options[0])
    selected_city = ctk.StringVar(value="All")
    selected_month = ctk.StringVar(value="All")
    unit_var = ctk.StringVar(value="Celsius")

    # Dropdowns
    chart_menu = ctk.CTkOptionMenu(top_frame, values=chart_options, variable=selected_chart, command=lambda _: draw_chart())
    chart_menu.pack(side="left", padx=10)

    city_menu = ctk.CTkOptionMenu(top_frame, values=["All"] + cities, variable=selected_city, command=lambda _: draw_chart())
    city_menu.pack(side="left", padx=10)

    month_menu = ctk.CTkOptionMenu(top_frame, values=["All"] + months, variable=selected_month, command=lambda _: draw_chart())
    month_menu.pack(side="left", padx=10)

    unit_menu = ctk.CTkOptionMenu(top_frame, values=["Celsius", "Fahrenheit"], variable=unit_var, command=lambda _: draw_chart())
    unit_menu.pack(side="left", padx=10)

    def to_fahrenheit(c):
        return c * 9 / 5 + 32

    def draw_chart():
        for widget in chart_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(8, 4.5))
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        ax.tick_params(axis='x', rotation=45)
        ax.tick_params(colors=text_color)

        # Apply filters
        city_filter = selected_city.get()
        month_filter = selected_month.get()
        use_fahrenheit = unit_var.get() == "Fahrenheit"

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
            ax.set_title("Monthly Avg Min/Max Temp", color=text_color)
            ax.set_ylabel("°F" if use_fahrenheit else "°C")

        elif option == "Total Monthly Precipitation":
            plot_cities = [city_filter] if city_filter != "All" else cities
            for city in plot_cities:
                city_data = filtered_df[filtered_df["city"] == city]
                monthly = city_data.groupby("month_str")["precip"].sum().reset_index()
                ax.plot(monthly["month_str"], monthly["precip"], marker="s", label=city, color=city_colors.get(city, "gray"))
            ax.set_title("Total Monthly Precipitation", color=text_color)
            ax.set_ylabel("Precipitation (mm or inch)")

        elif option == "Max Wind Speed by Month":
            plot_cities = [city_filter] if city_filter != "All" else cities
            for city in plot_cities:
                city_data = filtered_df[filtered_df["city"] == city]
                monthly = city_data.groupby("month_str")["max_wind_spd"].max().reset_index()
                ax.plot(monthly["month_str"], monthly["max_wind_spd"], marker="x", label=city, color=city_colors.get(city, "gray"))
            ax.set_title("Max Wind Speed by Month", color=text_color)
            ax.set_ylabel("Max Wind Speed")

        ax.legend(loc="upper left", fontsize="small")

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    draw_chart()

    # Back Button (with your button class)
    back_btn = create_button(
        parent_frame,
        text="← Back to Home",
        command=lambda: show_main_callback() if show_main_callback else None
    )
    back_btn.pack(pady=20)
