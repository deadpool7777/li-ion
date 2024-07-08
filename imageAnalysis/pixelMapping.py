import cv2

# Load the image
image_path = r"C:\Users\Alwin Soly\Desktop\li-ion\42452_2020_2675_Fig2_HTML.webp"
image = cv2.imread(image_path)

# Function to display coordinates on mouse click
def get_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordinates: ({x}, {y})")

# Display the image and set the mouse callback function
cv2.imshow('Image', image)
cv2.setMouseCallback('Image', get_coordinates)

# Wait until a key is pressed and close all windows
cv2.waitKey(0)
cv2.destroyAllWindows()
