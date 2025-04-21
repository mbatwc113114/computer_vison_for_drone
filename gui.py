import tkinter as tk
from tkinter import filedialog
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import contextily as ctx


class KMLViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KML Polygon Viewer")
        self.root.geometry("900x700")

        self.load_button = tk.Button(root, text="Load KML File", command=self.load_kml)
        self.load_button.pack(pady=10)

        # Label for area and perimeter
        self.info_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
        self.info_label.pack()

        self.canvas = None

    def load_kml(self):
        file_path = filedialog.askopenfilename(filetypes=[("KML Files", "*.kml")])
        if not file_path:
            return
        self.plot_kml(file_path)

    def plot_kml(self, file_path):
        # Read file
        gdf = gpd.read_file(file_path, driver="KML")

        # Reproject for plotting
        gdf_plot = gdf.to_crs(epsg=3857)

        # Reproject for accurate area/perimeter (e.g. India: EPSG:32643 - UTM zone 43N)
        gdf_metric = gdf.to_crs(epsg=32643)

        # Calculate area and perimeter
        total_area = gdf_metric.area.sum() / 1e6  # m² to km²
        total_perimeter = gdf_metric.length.sum() / 1000  # m to km

        # Update label
        self.info_label.config(
            text=f"Total Area: {total_area:.2f} km² | Total Perimeter: {total_perimeter:.2f} km"
        )

        # Plot
        fig, ax = plt.subplots(figsize=(8, 6))
        gdf_plot.plot(ax=ax, facecolor='none', edgecolor='red', linewidth=2)
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        ax.set_title("KML Polygon on Real Map")
        ax.axis("off")

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# Run it
if __name__ == "__main__":
    root = tk.Tk()
    app = KMLViewerApp(root)
    root.mainloop()
