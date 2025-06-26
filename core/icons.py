import requests
from PIL import Image, ImageTk
import io

def get_icon_image(icon_code):
    try:
        url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        response = requests.get(url)
        if response.status_code == 200:
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            return ImageTk.PhotoImage(image)
    except Exception as e:
        print("Error loading icon:", e)
    return None

def get_detail_icon(name):
    icons = {
        "Humidity": "\U0001F4A7",
        "Wind": "\U0001F32C",
        "Cloudiness": "\u2601",
        "Visibility": "\U0001F441",
    }
    return icons.get(name, "")
