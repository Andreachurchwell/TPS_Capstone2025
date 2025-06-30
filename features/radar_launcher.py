import os
import subprocess
import sys

def launch_radar_map(city, show_popup_callback):
    print(f"Launching radar for: {city}")
    """
    Launches the radar animation script using the given city.
    Calls show_popup_callback(title, message) if feedback is needed.
    """
    if city:
        radar_script = os.path.join("features", "radar_animated_map.py")
        subprocess.Popen([sys.executable, radar_script, city])
        show_popup_callback("Live Radar", "Radar opened in your browser.\nReturn to this app window when you're done.")
    else:
        show_popup_callback("Missing City", "Please enter a city before launching radar.")
