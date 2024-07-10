import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import re

# Load the image
# image_path = r"C:\Users\Alwin Soly\Desktop\li-ion\42452_2020_2675_Fig2_HTML.webp"
def find_pixel_ranges(image_path):
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Applying edge detection
        edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)

        # Detect lines using Hough Line Transform
        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

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

        # Drawing the detected corners on the image
        for corner in corners:
            cv2.circle(image, tuple(corner), 10, (0, 0, 255), -1)

        # Shows the image with detected corners
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

def extract_axis_range(image, axis):
    # Converting PIL image to NumPy array
    image_np = np.array(image)

    # Croping regions likely to contain axis labels
    height, width = image_np.shape[:2]
    if axis == 'x':
        crop_img = image_np[int(height * 0.9):height, :]  # Bottom part for x-axis
    elif axis == 'y':
        crop_img = image_np[:, 0:int(width * 0.1)]  # Left part for y-axis

    # Converting and applying adaptive thresholding
    gray_crop = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    thresh_crop = cv2.adaptiveThreshold(gray_crop, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Using pytesseract to extract text
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    text = pytesseract.image_to_string(thresh_crop, config=custom_config)

    # Finding all numbers in the text
    numbers = re.findall(r'-?\d+\.?\d*', text)
    if len(numbers) >= 2:
        numbers = sorted(map(float, numbers))
        return numbers[0], numbers[-1]
    else:
        return None

    




