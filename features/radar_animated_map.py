# import folium
# import webbrowser
# from geopy.geocoders import Nominatim

# def create_animated_radar_map(city_name):
#     # Get coordinates from city name
#     geolocator = Nominatim(user_agent="animated_radar_app")
#     location = geolocator.geocode(city_name)
#     if not location:
#         print("City not found.")
#         return

#     lat, lon = location.latitude, location.longitude

#     # Create base folium map
#     m = folium.Map(location=[lat, lon], zoom_start=7)

#     # Add city marker
#     folium.Marker([lat, lon], popup=city_name, icon=folium.Icon(color='blue')).add_to(m)

#     # Inject JS for radar animation
#     radar_js = f"""
#         <script>
#         var map = L.map('map', {{
#             center: [{lat}, {lon}],
#             zoom: 7
#         }});
#         L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
#             maxZoom: 19,
#         }}).addTo(map);

#         // Function to load RainViewer animation
#         var apiUrl = 'https://api.rainviewer.com/public/weather-maps.json';
#         fetch(apiUrl)
#             .then(response => response.json())
#             .then(data => {{
#                 var radarTimes = data.radar.past.map(t => t.time);
#                 var radarLayers = [];
#                 var currentFrame = 0;

#                 function addRadarFrame(time) {{
#                     return L.tileLayer(`https://tilecache.rainviewer.com/v2/radar/${{time}}/256/{{z}}/{{x}}/{{y}}/2/1_1.png`, {{
#                         opacity: 0.6
#                     }});
#                 }}

#                 // Preload all frames
#                 radarTimes.forEach(time => {{
#                     radarLayers.push(addRadarFrame(time));
#                 }});

#                 // Add first frame
#                 radarLayers[currentFrame].addTo(map);

#                 // Animate through radar frames
#                 setInterval(() => {{
#                     map.removeLayer(radarLayers[currentFrame]);
#                     currentFrame = (currentFrame + 1) % radarLayers.length;
#                     radarLayers[currentFrame].addTo(map);
#                 }}, 700);
#             }});
#         </script>
#     """

#     # Save map with radar JS injected
#     map_file = "animated_radar_map.html"
#     m.get_root().html.add_child(folium.Element(radar_js))
#     m.save(map_file)
#     webbrowser.open(map_file)

# # Example
# if __name__ == "__main__":
#     city = input("Enter city: ")
#     create_animated_radar_map(city)




import webbrowser

import os

def create_animated_radar_map(city_name):
    import requests
    from geopy.geocoders import Nominatim

    geolocator = Nominatim(user_agent="animated_radar_app")
    location = geolocator.geocode(city_name)
    if not location:
        print("City not found.")
        return

    lat, lon = location.latitude, location.longitude

    # HTML with full custom JS using RainViewer API
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Animated Radar Map</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
    </head>
    <body>
        <div id="map" style="width: 100%; height: 100vh;"></div>
        <script>
            var map = L.map('map').setView([{lat}, {lon}], 7);
                    L.marker([{lat}, {lon}]).addTo(map);

            L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 19
            }}).addTo(map);

            // RainViewer radar animation
            fetch('https://api.rainviewer.com/public/weather-maps.json')
                .then(response => response.json())
                .then(data => {{
                    var radarFrames = data.radar.past.map(f => f.time);
                    var layers = [];
                    var current = 0;

                    function getTileLayer(time) {{
                        return L.tileLayer(`https://tilecache.rainviewer.com/v2/radar/${{time}}/256/{{z}}/{{x}}/{{y}}/2/1_1.png`, {{
                            opacity: 0.6
                        }});
                    }}

                    radarFrames.forEach((t, i) => {{
                        layers.push(getTileLayer(t));
                    }});

                    layers[current].addTo(map);
                    setInterval(() => {{
                        map.removeLayer(layers[current]);
                        current = (current + 1) % layers.length;
                        layers[current].addTo(map);
                    }}, 700);
                }});
        </script>
    </body>
    </html>
    """

    html_path = os.path.join(os.path.dirname(__file__), "animated_radar_map.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    webbrowser.open_new(html_path)

# # Run it
# if __name__ == "__main__":
#     city = input("Enter a city: ")
#     create_animated_radar_map(city)


import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:])
        create_animated_radar_map(city)
    else:
        print("No city provided.")


