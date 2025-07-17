



# import os
# import webbrowser
# from geopy.geocoders import Nominatim

# # New function that uses coordinates directly
# def launch_radar_map_by_coords(lat, lon):
#     html_template = f"""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Animated Radar Map</title>
#         <meta charset="utf-8" />
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
#         <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
#     </head>
#     <body>
#         <div id="map" style="width: 100%; height: 700px;"></div>
#         <script>
#             var map = L.map('map').setView([{lat}, {lon}], 7);
#             L.marker([{lat}, {lon}]).addTo(map);
#             L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
#                 maxZoom: 19
#             }}).addTo(map);



#             fetch('https://api.rainviewer.com/public/weather-maps.json')
#                 .then(response => response.json())
#                 .then(data => {{
#                     var radarFrames = data.radar.past.map(f => f.time);
#                     var layers = [];
#                     var current = 0;

#                     function getTileLayer(time) {{
#                         return L.tileLayer(`https://tilecache.rainviewer.com/v2/radar/${{time}}/256/{{z}}/{{x}}/{{y}}/2/1_1.png`, {{
#                             opacity: 0.6
#                         }});
#                     }}

#                     radarFrames.forEach((t, i) => {{
#                         layers.push(getTileLayer(t));
#                     }});

#                     layers[current].addTo(map);
#                     setInterval(() => {{
#                         map.removeLayer(layers[current]);
#                         current = (current + 1) % layers.length;
#                         layers[current].addTo(map);
#                     }}, 700);
#                 }});
#         </script>
#     </body>
#     </html>
#     """

#     html_path = os.path.join(os.path.dirname(__file__), "animated_radar_map.html")
#     with open(html_path, "w", encoding="utf-8") as f:
#         f.write(html_template)

#     webbrowser.open_new(html_path)

# # This still lets you launch by city name
# def launch_radar_map_by_name(city_name):
#     geolocator = Nominatim(user_agent="animated_radar_app")
#     location = geolocator.geocode(city_name)
#     if not location:
#         print(f"City '{city_name}' not found.")
#         return
#     launch_radar_map_by_coords(location.latitude, location.longitude)


# import os
# import webbrowser
# from geopy.geocoders import Nominatim
# from dotenv import load_dotenv

# # Load API key safely
# load_dotenv()
# API_KEY = os.getenv("OPENWEATHER_API_KEY")

# def launch_radar_map_by_coords(lat, lon):
#     html_template = f"""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Animated Radar Map with Layers</title>
#         <meta charset="utf-8" />
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
#         <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
#         <style>
#             #map {{ height: 100vh; width: 100%; }}
#             .leaflet-control-layers-overlays label {{ color: #000; }}
#         </style>
#     </head>
#     <body>
#         <div id="map"></div>
#         <script>
#             var map = L.map('map').setView([{lat}, {lon}], 7);

#             // Base layer (OpenStreetMap)
#             var baseLayer = L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
#                 maxZoom: 19,
#                 attribution: '&copy; OpenStreetMap'
#             }}).addTo(map);

#             // Marker at center
#             L.marker([{lat}, {lon}]).addTo(map);

#             // --- OpenWeather overlay layers ---
#             const apiKey = "{API_KEY}";

#             var clouds = L.tileLayer(`https://tile.openweathermap.org/map/clouds_new/{{z}}/{{x}}/{{y}}.png?appid=${{apiKey}}`, {{ opacity: 0.5 }});
#             var temp = L.tileLayer(`https://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid=${{apiKey}}`, {{ opacity: 0.5 }});
#             var wind = L.tileLayer(`https://tile.openweathermap.org/map/wind_new/{{z}}/{{x}}/{{y}}.png?appid=${{apiKey}}`, {{ opacity: 0.5 }});
#             var radarOverlay = L.layerGroup();

#             // --- RainViewer radar animation ---
#             fetch('https://api.rainviewer.com/public/weather-maps.json')
#                 .then(response => response.json())
#                 .then(data => {{
#                     var radarFrames = data.radar.past.map(f => f.time);
#                     var layers = [];
#                     var current = 0;

#                     function getTileLayer(time) {{
#                         return L.tileLayer(`https://tilecache.rainviewer.com/v2/radar/${{time}}/256/{{z}}/{{x}}/{{y}}/2/1_1.png`, {{
#                             opacity: 0.6
#                         }});
#                     }}

#                     radarFrames.forEach(time => {{
#                         layers.push(getTileLayer(time));
#                     }});

#                     layers[current].addTo(radarOverlay);
#                     radarOverlay.addTo(map);

#                     setInterval(() => {{
#                         radarOverlay.clearLayers();
#                         current = (current + 1) % layers.length;
#                         radarOverlay.addLayer(layers[current]);
#                     }}, 700);
#                 }});

#             // Layer controls
#             var overlays = {{
#                 "Clouds": clouds,
#                 "Temperature": temp,
#                 "Wind": wind,
#                 "Radar Animation": radarOverlay
#             }};
#             L.control.layers(null, overlays).addTo(map);
#         </script>
#     </body>
#     </html>
#     """

#     html_path = os.path.join(os.path.dirname(__file__), "animated_radar_map.html")
#     with open(html_path, "w", encoding="utf-8") as f:
#         f.write(html_template)

#     webbrowser.open_new_tab("file://" + os.path.abspath(html_path))

# def launch_radar_map_by_name(city_name):
#     geolocator = Nominatim(user_agent="animated_radar_app")
#     location = geolocator.geocode(city_name)
#     if not location:
#         print(f"City '{city_name}' not found.")
#         return
#     launch_radar_map_by_coords(location.latitude, location.longitude)



import os
import webbrowser
from geopy.geocoders import Nominatim
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")


def launch_radar_map_by_coords(lat, lon):
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Radar + OpenWeather Layers</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        <style>
            body {{
                margin: 0;
                padding: 0;
            }}
            #map {{
                height: 100vh;
            }}
            .layer-toggle {{
                position: absolute;
                top: 10px;
                left: 10px;
                background: #1e1e1e;
                color: white;
                padding: 12px;
                border-radius: 8px;
                z-index: 1001;
                font-family: sans-serif;
                max-height: 90vh;
                overflow-y: auto;
                box-shadow: 0 0 10px rgba(0,0,0,0.5);
            }}
            .layer-toggle h4 {{
                margin: 10px 0 4px;
                font-size: 14px;
                border-bottom: 1px solid #444;
            }}
            .layer-toggle label {{
                display: block;
                margin: 4px 0;
                font-size: 13px;
            }}
            .layer-toggle input[type="checkbox"] {{
                accent-color: orange;
                width: 16px;
                height: 16px;
                cursor: pointer;
            }}
        </style>
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    </head>
    <body>
        <div class="layer-toggle">
            <h4>Radar</h4>
            <label><input type="checkbox" id="radarLayer" checked> RainViewer Radar</label>

            <h4>Clouds</h4>
            <label><input type="checkbox" id="cloudsNew"> Clouds (new)</label>
            <label><input type="checkbox" id="cloudsOld"> Clouds (classic)</label>

            <h4>Precipitation</h4>
            <label><input type="checkbox" id="precipNew"> Precipitation (new)</label>
            <label><input type="checkbox" id="precipOld"> Precipitation (classic)</label>

            <h4>Temperature</h4>
            <label><input type="checkbox" id="tempNew"> Temperature (new)</label>
            <label><input type="checkbox" id="tempOld"> Temperature (classic)</label>

            <h4>Wind</h4>
            <label><input type="checkbox" id="windNew"> Wind (new)</label>
            <label><input type="checkbox" id="windOld"> Wind (classic)</label>

            <h4>Pressure</h4>
            <label><input type="checkbox" id="pressureNew"> Pressure (new)</label>
            <label><input type="checkbox" id="pressureOld"> Pressure (classic)</label>

            <h4>Snow</h4>
            <label><input type="checkbox" id="snowOld"> Snow (classic)</label>
        </div>

        <div id="map"></div>
        <script>
            const map = L.map('map', {{
                zoomControl: false
            }}).setView([{lat}, {lon}], 7);
            L.control.zoom({{ position: 'bottomright' }}).addTo(map);

            const baseLayer = L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
            L.marker([{lat}, {lon}]).addTo(map);

            const apiKey = "{API_KEY}";
            const layers = {{
                cloudsNew: L.tileLayer(`https://tile.openweathermap.org/map/clouds_new/{{z}}/{{x}}/{{y}}.png?appid=${{apiKey}}`, {{opacity: 0.5}}),
                cloudsOld: L.tileLayer(`https://tile.openweathermap.org/map/clouds/{{z}}/{{x}}/{{y}}.png?appid=${{apiKey}}`, {{opacity: 0.5}}),
                precipNew: L.tileLayer(`https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid=${{apiKey}}`, {{opacity: 0.5}}),
                precipOld: L.tileLayer(`https://tile.openweathermap.org/map/precipitation/{{z}}/{{x}}/{{y}}.png?appid=${{apiKey}}`, {{opacity: 0.5}}),
                tempNew: L.tileLayer(`https://tile.openweathermap.org/map/temp_new/{{z}}/{{x}}/{{y}}.png?appid=${{apiKey}}`, {{opacity: 0.5}}),
                tempOld: L.tileLayer(`https://tile.openweathermap.org/map/temp/{{z}}/{{x}}/{{y}}.png?appid=${{apiKey}}`, {{opacity: 0.5}}),
                windNew: L.tileLayer(`https://tile.openweathermap.org/map/wind_new/{{z}}/{{x}}/{{y}}.png?appid=${{apiKey}}`, {{opacity: 0.5}}),
                windOld: L.tileLayer(`https://tile.openweathermap.org/map/wind/{{z}}/{{x}}/{{y}}.png?appid=${{apiKey}}`, {{opacity: 0.5}}),
                pressureNew: L.tileLayer(`https://tile.openweathermap.org/map/pressure_new/{{z}}/{{x}}/{{y}}.png?appid=${{apiKey}}`, {{opacity: 0.5}}),
                pressureOld: L.tileLayer(`https://tile.openweathermap.org/map/pressure/{{z}}/{{x}}/{{y}}.png?appid=${{apiKey}}`, {{opacity: 0.5}}),
                snowOld: L.tileLayer(`https://tile.openweathermap.org/map/snow/{{z}}/{{x}}/{{y}}.png?appid=${{apiKey}}`, {{opacity: 0.5}})
            }};

            let radarFrames = [], radarLayers = [], radarCurrent = 0, radarTimer;
            function startRadar() {{
                fetch('https://api.rainviewer.com/public/weather-maps.json')
                    .then(res => res.json())
                    .then(data => {{
                        radarFrames = data.radar.past.map(f => f.time);
                        radarLayers = radarFrames.map(time =>
                            L.tileLayer(`https://tilecache.rainviewer.com/v2/radar/${{time}}/256/{{z}}/{{x}}/{{y}}/2/1_1.png`, {{ opacity: 0.6 }})
                        );
                        radarLayers[radarCurrent].addTo(map);
                        radarTimer = setInterval(() => {{
                            map.removeLayer(radarLayers[radarCurrent]);
                            radarCurrent = (radarCurrent + 1) % radarLayers.length;
                            map.addLayer(radarLayers[radarCurrent]);
                        }}, 700);
                    }});
            }}

            function stopRadar() {{
                if (radarTimer) {{
                    clearInterval(radarTimer);
                    radarLayers.forEach(l => map.removeLayer(l));
                }}
            }}

            document.getElementById('radarLayer').addEventListener('change', e => {{
                e.target.checked ? startRadar() : stopRadar();
            }});

            Object.keys(layers).forEach(key => {{
                const checkbox = document.getElementById(key);
                if (checkbox) {{
                    checkbox.addEventListener('change', e => {{
                        e.target.checked ? layers[key].addTo(map) : map.removeLayer(layers[key]);
                    }});
                }}
            }});

            startRadar();
        </script>
    </body>
    </html>
    """

    html_path = os.path.join(os.path.dirname(__file__), "animated_radar_map.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    webbrowser.open_new_tab("file://" + os.path.abspath(html_path))



def launch_radar_map_by_name(city_name):
    geolocator = Nominatim(user_agent="animated_radar_app")
    location = geolocator.geocode(city_name)
    if location:
        launch_radar_map_by_coords(location.latitude, location.longitude)
