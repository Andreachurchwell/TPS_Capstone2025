import requests # used to make http req to download icons
from PIL import Image, ImageTk #pillow for image processing and tk compatibility
import io #used to handle byte streams for downloaded img

def get_icon_image(icon_code):
        # """
        # downloads the weather icon image based on the icon code from openweather converts
        #   it into a format tkinter can use(photoimage)
        #   """
    try:
# using icon endpoint from openweather
        url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        # send req to get icon
        response = requests.get(url)
        # if succesful convert to tkinter compat image
        if response.status_code == 200:
            image_data = response.content #raw image bytes
            image = Image.open(io.BytesIO(image_data)) #open img from bytes

            resized_image = image.resize((80, 80), Image.LANCZOS)
            return ImageTk.PhotoImage(resized_image) #convert to photoimg for tk
    except Exception as e:
        print("Error loading icon:", e) #handles any issues
    return None #returns none if image cant be fetched

# def get_detail_icon(name):
#     # returns unicode emojis for weather dets
#     icons = {
#         "Humidity": "\U0001F4A7",
#         "Wind": "\U0001F32C",
#         "Cloudiness": "\u2601",
#         "Visibility": "\U0001F441",
#     }
#     return icons.get(name, "")

def get_detail_icon(name):
    icons = {
        "Humidity": "💧",
        "Wind": "💨",
        "Cloudiness": "☁️",
        "Visibility": "👁️",
        "Feels Like": "🌡️",
        "Pressure": "📊",
        "Rain": "🌧️",
        "Gust": "🌬️",
        "Sunrise": "🌅"
    }
    return icons.get(name, "")
