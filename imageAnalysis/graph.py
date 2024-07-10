import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Load the image
image_path = r"C:\Users\Alwin Soly\Desktop\42452_2020_2675_Fig2_HTML.webp"
image = Image.open(image_path)
image_np = np.array(image)

# Convert the original image to HSV (Hue, Saturation, Value) color space for color segmentation
hsv_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)

# Define color ranges for each line color in HSV
color_ranges = {
    '1000 mA': ([100, 150, 0], [140, 255, 255]),  # Blue
    '500 mA': ([10, 100, 100], [25, 255, 255]),   # Orange
    '200 mA': ([25, 50, 70], [35, 255, 255]),     # Yellow
    '100 mA': ([140, 50, 50], [160, 255, 255]),   # Purple
    '50 mA': ([40, 40, 40], [70, 255, 255]),      # Green
    '20 mA': ([20, 150, 150], [30, 255, 255])     # Light Orange (approximated)
}

# Create masks for each color and extract pixel coordinates
line_coordinates = {}
for label, (lower, upper) in color_ranges.items():
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    
    # Create a mask for the color range
    mask = cv2.inRange(hsv_image, lower, upper)
    
    # Find contours (which should correspond to the lines)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Extract coordinates for the largest contour (assumed to be the relevant line)
    if contours:
        contour = max(contours, key=cv2.contourArea)
        line_coordinates[label] = contour

# Define the axis ranges from the graph
x_range = (-10000, 0)
y_range = (2.8, 4.2)

# Get the dimensions of the image
height, width, _ = image_np.shape

# Define the pixel ranges for the graph (manually approximated from the image)
# These should ideally be set precisely based on the graph's pixel coordinates
pixel_x_range = (107, 960) 
pixel_y_range = (665, 16)  

# Function to map pixel coordinates to graph coordinates
def pixel_to_graph_coords(x_pixel, y_pixel):
    x_graph = np.interp(x_pixel, pixel_x_range, x_range)
    y_graph = np.interp(y_pixel, pixel_y_range, y_range)
    return x_graph, y_graph

# Extract graph coordinates for each line
graph_data = {}
for label, contour in line_coordinates.items():
    contour = contour.squeeze()
    graph_coords = [pixel_to_graph_coords(x, y) for x, y in contour]
    graph_data[label] = np.array(graph_coords)

# Plot the graph coordinates to verify the transformation
plt.figure(figsize=(10, 8))
for label, coords in graph_data.items():
    plt.plot(coords[:, 0], coords[:, 1], label=label)

plt.xlabel('Capacity (mAh)')
plt.ylabel('Cell Voltage (V)')
plt.title('Graph Coordinates')
plt.legend()
plt.grid(True)
plt.show()
