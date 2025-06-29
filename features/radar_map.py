import folium
import webbrowser
from geopy.geocoders import Nominatim

def create_radar_map(city_name):
    # Get coordinates using geopy
    geolocator = Nominatim(user_agent="radar_map_app")
    location = geolocator.geocode(city_name)

    if location:
        lat, lon = location.latitude, location.longitude
    else:
        print("City not found.")
        return

    # Create folium map
    m = folium.Map(location=[lat, lon], zoom_start=7)

    # Add RainViewer radar tile layer
    folium.raster_layers.TileLayer(
        tiles='https://tilecache.rainviewer.com/v2/radar/now/256/{z}/{x}/{y}/2/1_1.png',
        attr='RainViewer',
        name='Live Weather Radar',
        overlay=True,
        control=True,
        opacity=0.6
    ).add_to(m)

    # Add city marker
    folium.Marker([lat, lon], popup=city_name, icon=folium.Icon(color='blue')).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Save and open in browser
    map_file = "radar_map.html"
    m.save(map_file)
    webbrowser.open(map_file)

# Example usage
if __name__ == "__main__":
    city = input("Enter city name: ")
    create_radar_map(city)
