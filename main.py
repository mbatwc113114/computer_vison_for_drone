# import geopandas as gpd
# from shapely.geometry import LineString
# import matplotlib.pyplot as plt
# import numpy as np

# def slice_area_for_drone_path(gdf, view_width):
#     """
#     Slices a polygon area into vertical strips based on the drone's camera view width.
#     Returns sliced path lines as a GeoDataFrame.
#     """
#     # Ensure CRS is projected in meters
#     if gdf.crs.to_epsg() != 3857:
#         gdf = gdf.to_crs(epsg=3857)

#     # Get bounds of the area
#     minx, miny, maxx, maxy = gdf.total_bounds
#     width = maxx - minx

#     # Calculate number of slices
#     num_slices = int(np.ceil(width / view_width))

#     # Create vertical slicing lines
#     lines = []
#     for i in range(num_slices + 1):
#         x = minx + i * view_width
#         line = LineString([(x, miny), (x, maxy)])
#         lines.append(line)

#     # Convert to GeoDataFrame
#     line_gdf = gpd.GeoDataFrame(geometry=lines, crs=gdf.crs)

#     # Clip the lines to the area of interest
#     sliced_paths = gpd.overlay(line_gdf, gdf, how='intersection')

#     return sliced_paths

# # ---------------- MAIN SCRIPT ----------------

# # 1. Load the KML file
# gdf = gpd.read_file("gsv.kml", driver='KML')

# # 2. Convert to a projected CRS (meters)
# gdf = gdf.to_crs(epsg=3857)

# # 3. Create sliced paths (e.g., 20m camera width)
# path_gdf = slice_area_for_drone_path(gdf, view_width=20)

# # 4. Plot using matplotlib
# fig, ax = plt.subplots(figsize=(10, 10))
# gdf.plot(ax=ax, color='lightgreen', edgecolor='black', linewidth=1)
# path_gdf.plot(ax=ax, color='red', linewidth=1)

# # 5. Customize plot
# plt.title("Drone Flight Path Over KML Area", fontsize=14)
# plt.xlabel("X (meters)")
# plt.ylabel("Y (meters)")
# plt.grid(True)
# plt.axis("equal")
# plt.tight_layout()

# # 6. Show plot
# plt.show()


import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx  # for basemap tiles

# 1. Load KML polygon
gdf = gpd.read_file("daku.kml", driver='KML')

# 2. Project to Web Mercator (EPSG:3857), required by contextily
gdf = gdf.to_crs(epsg=3857)

# 3. Plot with basemap
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, facecolor='none', edgecolor='red', linewidth=2)

# 4. Add basemap (OpenStreetMap)
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

# 5. Add titles and show
plt.title("KML Polygon Overlay on Real Map")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.tight_layout()
plt.show()
