from tkintermapview import TkinterMapView
import tkinter as tk

class MapFeature:
    def __init__(self, parent):
        self.map_widget = TkinterMapView(parent, width=500, height=300, corner_radius=10)
        self.map_widget.set_position(35.0, -90.0)  # Default location
        self.map_widget.set_zoom(6)
        self.map_widget.pack(pady=10)

    def update_location(self, lat, lon):
        self.map_widget.set_position(lat, lon)
        self.map_widget.set_zoom(10)

    def destroy(self):
        try:
            self.map_widget.canvas.delete("all")  # Clear canvas updates
        except Exception as e:
            print("Canvas cleanup skipped:", e)
        try:
            self.map_widget.destroy()  # Properly destroy map widget
        except Exception as e:
            print("MapFeature cleanup error:", e)


