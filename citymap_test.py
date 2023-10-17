import geopandas as gpd
import osmnx as ox
import matplotlib.pyplot as plt
import cv2  # Import OpenCV

# Define the city of Porto as the place of interest
place_name = "Barcelona, Spain"

# Retrieve the street network for Porto
graph = ox.graph_from_place(place_name, network_type="all")

# Create a GeoDataFrame from the street network
gdf = ox.graph_to_gdfs(graph, nodes=False, edges=True)

# Define the latitude and longitude coordinates
latitude = 41.147355
longitude = -8.666995

# Find the nearest node to the given coordinates
nearest_node = ox.distance.nearest_nodes(graph, longitude, latitude, return_dist=False)

# Get the coordinates (latitude and longitude) of the nearest node
node_data = graph.nodes[nearest_node]
node_latitude = node_data['y']
node_longitude = node_data['x']

# Create a figure with a white background
fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')

# Plot the map in black and white
gdf.plot(ax=ax, color='black', linewidth=0.5)

# Remove axes
ax.axis('off')

# Set an extremely high DPI for the best quality (e.g., 1200)
plt.savefig("Barcelona_map.png", dpi=1200, bbox_inches='tight', pad_inches=0)

# Read and display the saved image with OpenCV
image = cv2.imread("porto_map_best_quality.png")

# Calculate the pixel coordinates of the pinpoint based on the nearest node
x = int((node_data['x'] - gdf.bounds.minx.min()) / (gdf.bounds.maxx.max() - gdf.bounds.minx.min()) * image.shape[1])
y = int((1 - (node_data['y'] - gdf.bounds.miny.min()) / (gdf.bounds.maxy.max() - gdf.bounds.miny.min())) * image.shape[0])

# Draw a red circle (pinpoint) on the image at the calculated pixel coordinates
cv2.circle(image, (x, y), 5, (0, 0, 255), -1)  # (0, 0, 255) is the color (red)

while True:
    cv2.imshow("Porto Map with Pinpoint", image)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close all OpenCV windows
cv2.destroyAllWindows()
