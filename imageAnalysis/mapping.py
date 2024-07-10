import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from pixelMappingAutomation import find_pixel_ranges, extract_axis_range

# Load the image
image_path = r"C:\Users\Alwin Soly\Desktop\li-ion\li-ion\imageAnalysis\42452_2020_2675_Fig2_HTML.webp"
image = Image.open(image_path)
image_np = np.array(image)

# Converting the original image to HSV (Hue, Saturation, Value) color space for color segmentation
hsv_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)

# Defining color ranges for each line color in HSV
color_ranges = {
    '1000 mA': ([100, 150, 0], [140, 255, 255]),  # Blue
    # '500 mA': ([10, 100, 100], [25, 255, 255]),   # Orange
    # '200 mA': ([25, 50, 70], [35, 255, 255]),     # Yellow
    # '100 mA': ([140, 50, 50], [160, 255, 255]),   # Purple
    # '50 mA': ([40, 40, 40], [70, 255, 255]),      # Green
    # '20 mA': ([20, 150, 150], [30, 255, 255])     # Light Orange (approximated)
}

# Creating masks for each color and extract pixel coordinates
line_coordinates = {}
for label, (lower, upper) in color_ranges.items():
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    
    # Creating a mask for the color range
    mask = cv2.inRange(hsv_image, lower, upper)
    
    # Find contours (which should correspond to the lines)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Extracting coordinates for the largest contour (assumed to be the relevant line)
    if contours:
        contour = max(contours, key=cv2.contourArea)
        line_coordinates[label] = contour

# Draw the contours on the image for verification
output_image = image_np.copy()
for label, contour in line_coordinates.items():
    cv2.drawContours(output_image, [contour], -1, (0, 255, 0), 2)  # Draw contour in green

#Show the image with contours
# plt.figure(figsize=(10, 8))
# plt.imshow(output_image)
# plt.title('Image with Contours')
# plt.axis('off')
# plt.show()

pixel_x_range, pixel_y_range = find_pixel_ranges(image_path)
    # Extract x and y axis ranges using OCR
x_range = extract_axis_range(image, 'x')
y_range = extract_axis_range(image, 'y')
y_range = (y_range[1], y_range[0])

print(f"X Range: {x_range}")
print(f"Y Range: {y_range}")

#Function to map pixel coordinates to graph coordinates
def pixel_to_graph_coords(x_pixel, y_pixel):
    # pixel_x_range = (107, 961)
    # pixel_y_range = (16, 666)
    # pixel_x_range = (110, 958)
    # pixel_y_range = (21, 617)
    # x_range = (-12000, 0)
    # y_range = (4.2, 2.8)
    x_graph = np.interp(x_pixel, pixel_x_range, x_range)
    y_graph = np.interp(y_pixel, pixel_y_range, y_range)
    return x_graph, y_graph

# # Extraction of graph coordinates for each line
graph_data = {}
for label, contour in line_coordinates.items():
    contour = contour.squeeze()
    graph_coords = [pixel_to_graph_coords(x, y) for x, y in contour]
    graph_data[label] = np.array(graph_coords)


# # Sampling the data to reduce the number of points
def sample_data(data, num_samples):
    if len(data) > num_samples:
        indices = np.linspace(0, len(data) - 1, num_samples).astype(int)
        return data[indices]
    return data

num_samples = 100  # Desired number of samples
sampled_graph_data = {label: sample_data(coords, num_samples) for label, coords in graph_data.items()}

# # Ploting the graph coordinates to verify the transformation
plt.figure(figsize=(10, 8))
for label, coords in graph_data.items():
    plt.scatter(coords[:, 0], coords[:, 1], label=label, s=1)  # Use scatter plot for detailed inspection

plt.xlabel('Capacity (mAh)')
plt.ylabel('Cell Voltage (V)')
plt.title('Graph Coordinates')
plt.legend()
plt.grid(True)
plt.show()

# Saving the graph coordinates to a CSV file
rows = []
for label, coords in sampled_graph_data.items():
    for x, y in coords:
        rows.append([label, x, y])

# # Creating a DataFrame
df = pd.DataFrame(rows, columns=['Label', 'Capacity (mAh)', 'Cell Voltage (V)'])

#Saving to CSV
output_csv_path = r"C:\Users\Alwin Soly\Desktop\graph_coordinates.csv"
df.to_csv(output_csv_path, index=False)

print(f"Graph coordinates saved to {output_csv_path}")
