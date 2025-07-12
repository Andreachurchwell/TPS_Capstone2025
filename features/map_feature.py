from tkintermapview import TkinterMapView


class MapFeature:
    def __init__(self, parent):
        self.map_widget = TkinterMapView(parent, width=500, height=300, corner_radius=10)
        self.map_widget.set_position(35.0, -90.0)
        self.map_widget.set_zoom(6)
        self.map_widget.pack(pady=10)

    def update_location(self, lat, lon):
        self.map_widget.set_position(lat, lon)
        self.map_widget.set_zoom(10)

    def set_tile_server(self, tile_url):
        try:
            self.map_widget.set_tile_server(tile_url)
            print(f"[DEBUG] Tile switched to: {tile_url}")
            # Force map to refresh visually
            self.map_widget.set_zoom(self.map_widget.zoom + 0.1)
            self.map_widget.set_zoom(self.map_widget.zoom - 0.1)
        except Exception as e:
            print("[ERROR] Failed to set tile server:", e)

    def destroy(self):
        try:
            self.map_widget.canvas.delete("all")
        except Exception as e:
            print("Canvas cleanup skipped:", e)
        try:
            self.map_widget.destroy()
        except Exception as e:
            print("MapFeature cleanup error:", e)


