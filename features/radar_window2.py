import webbrowser
from geopy.geocoders import Nominatim

def create_animated_radar_map(city_name):
    geolocator = Nominatim(user_agent="radar_app")
    location = geolocator.geocode(city_name)
    if not location:
        print("City not found.")
        return

    lat, lon = location.latitude, location.longitude

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Live Radar</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    </head>
    <body style="margin:0">
        <div id="map" style="width: 100%; height: 100vh;"></div>
        <script>
            var map = L.map('map').setView([{lat}, {lon}], 7);
            L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 19,
            }}).addTo(map);

            var radar = L.tileLayer('https://tilecache.rainviewer.com/v2/radar/nowcast/0/512/{{z}}/{{x}}/{{y}}/2/1_1.png', {{
                opacity: 0.6,
                zIndex: 10
            }}).addTo(map);
        </script>
    </body>
    </html>
    """

    file_path = "live_radar.html"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html)

    webbrowser.open(file_path)

