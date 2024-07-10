import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import re
import os
from PIL import Image
import pandas as pd

# Function to find pixel ranges for x and y axes
def find_pixel_ranges(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Applying edge detection
    edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)

    # Detect lines using Hough Line Transform
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    if lines is None:
        print("No lines detected. Adjust parameters or check input image.")
        return None

    # Function to find corners based on line endpoints
    def find_corners(lines):
        corners = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Filter lines based on slope and position within image boundaries
            if abs(y2 - y1) > 5 and abs(x2 - x1) > 5:
                corners.extend([(x1, y1), (x2, y2)])
        return corners

    # Extracting corners from lines
    corners = find_corners(lines)

    # Converting corners to numpy array
    corners = np.array(corners)

    if corners.shape[0] == 0:
        print("No valid corners found. Adjust find_corners function or input image.")
        return None

    # Debug statement to print corners and its shape
    print("Corners:", corners)
    print("Corners shape:", corners.shape)

    # Drawing the detected corners on the image (for visualization)
    for corner in corners:
        cv2.circle(image, tuple(corner), 10, (0, 0, 255), -1)

    # Shows the image with detected corners (for verification)
    plt.figure(figsize=(10, 8))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Image with Detected Corners')
    plt.axis('off')
    plt.show()

    # Determining the pixel ranges for x and y axes
    x1 = np.min(corners[:, 0])
    x2 = np.max(corners[:, 0])
    y1 = np.min(corners[:, 1])
    y2 = np.max(corners[:, 1])

    print(f"Pixel X Range: ({x1}, {x2})")
    print(f"Pixel Y Range: ({y1}, {y2})")

    return (x1, x2), (y1, y2)

# Function to extract axis range using OCR (Optical Character Recognition)
def extract_axis_range(image, axis):
    # Convert PIL image to OpenCV format
    image_np = np.array(image)

    # Crop regions likely to contain axis labels
    height, width = image_np.shape[:2]
    if axis == 'x':
        crop_img = image_np[int(height * 0.9):height, :]  # Bottom part for x-axis
    elif axis == 'y':
        crop_img = image_np[:, 0:int(width * 0.1)]  # Left part for y-axis

    # Convert and apply adaptive thresholding
    gray_crop = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    thresh_crop = cv2.adaptiveThreshold(gray_crop, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Use pytesseract to extract text
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    text = pytesseract.image_to_string(thresh_crop, config=custom_config)

    # Find all numbers in the text
    numbers = re.findall(r'-?\d+\.?\d*', text)
    if len(numbers) >= 2:
        numbers = sorted(map(float, numbers))
        return numbers[0], numbers[-1]
    else:
        return None

# Function to map pixel coordinates to graph coordinates
def pixel_to_graph_coords(x_pixel, y_pixel, pixel_x_range, pixel_y_range, x_range, y_range):
    x_graph = np.interp(x_pixel, pixel_x_range, x_range)
    y_graph = np.interp(y_pixel, pixel_y_range, y_range)
    return x_graph, y_graph

# Function to sample data to reduce the number of points
def sample_data(data, num_samples):
    if len(data) > num_samples:
        indices = np.linspace(0, len(data) - 1, num_samples).astype(int)
        return data[indices]
    return data

# Main function to process each graph image
def process_graph_image(image_path, output_csv_path):
    # Load the image
    image = Image.open(image_path)
    image_np = np.array(image)

    # Find pixel ranges for x and y axes
    pixel_ranges = find_pixel_ranges(image_path)
    if pixel_ranges is None:
        print(f"Skipping {image_path} due to no valid corners.")
        return

    pixel_x_range, pixel_y_range = pixel_ranges

    # Extract x and y axis ranges using OCR
    x_range = extract_axis_range(image, 'x')
    y_range = extract_axis_range(image, 'y')
    if y_range:
        y_range = (y_range[1], y_range[0])  # Invert y_range (assuming it's top to bottom)

    # Initialize dictionary to store graph data
    graph_data = {}

    # Example color ranges (replace with actual color segmentation)
    color_ranges = {
        'GraphElement1': ([0, 0, 0], [255, 255, 255])  # Replace with actual color ranges
    }

    for label, (lower, upper) in color_ranges.items():
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        # Create a mask for the color range
        mask = cv2.inRange(image_np, lower, upper)

        # Find contours (which should correspond to the lines)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Extract coordinates for the largest contour (assumed to be the relevant line)
        if contours:
            contour = max(contours, key=cv2.contourArea)
            contour = contour.squeeze()

            # Map pixel coordinates to graph coordinates
            graph_coords = [pixel_to_graph_coords(x, y, pixel_x_range, pixel_y_range, x_range, y_range) for x, y in contour]

            # Sample data points to reduce the number of points
            graph_data[label] = sample_data(np.array(graph_coords), num_samples=100)

    # Create rows for CSV file
    rows = []
    for label, coords in graph_data.items():
        for x, y in coords:
            rows.append([label, x, y])

    # Create DataFrame
    df = pd.DataFrame(rows, columns=['Label', 'X Coordinate', 'Y Coordinate'])

    # Save to CSV file
    if not os.path.exists(output_csv_path):
        df.to_csv(output_csv_path, index=False)
    else:
        df.to_csv(output_csv_path, mode='a', header=False, index=False)

# Main script to iterate through each graph image and process
graph_folder = r"C:\Users\Alwin Soly\Desktop\li-ion\li-ion\graphs"
output_csv_folder = r"C:\Users\Alwin Soly\Desktop\li-ion\li-ion\CSV files"

# Ensure output folder exists
if not os.path.exists(output_csv_folder):
    os.makedirs(output_csv_folder)

# Process each image in the graph folder
for image_name in os.listdir(graph_folder):
    image_path = os.path.join(graph_folder, image_name)
    output_csv_path = os.path.join(output_csv_folder, f"{os.path.splitext(image_name)[0]}.csv")
    process_graph_image(image_path, output_csv_path)

print("Graph coordinates saved to CSV files in:", output_csv_folder)
