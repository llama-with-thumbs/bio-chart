import cv2
import numpy as np
import matplotlib.pyplot as plt

def calculate_object_perimeter_path(image_path='test.jpg', epsilon_factor=0.005):
    # Load the image from the given path or use 'test.jpg' by default
    image = cv2.imread(image_path)

    # Convert the image to HSV color space to better detect the green color
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of green color in HSV
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])

    # Create a mask for green objects
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Apply minimal Gaussian Blur (using a small kernel size for minimal smoothing)
    mask = cv2.GaussianBlur(mask, (3, 3), 0)

    # Find contours in the masked grayscale image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Variable to store the simplified contour points (path)
    path = []

    # Loop through each contour, approximate the contour with fewer points
    for contour in contours:
        # Calculate the epsilon value based on the contour's perimeter
        epsilon = epsilon_factor * cv2.arcLength(contour, True)  # Smaller epsilon_factor for less approximation
        approx = cv2.approxPolyDP(contour, epsilon, True)  # Approximate the contour

        # Extract the simplified (x, y) coordinates
        for point in approx:
            x, y = point[0]  # Extract x and y coordinates
            path.append((x, y))

        # Optionally: Draw the simplified perimeter path on the original image for visualization
        cv2.drawContours(image, [approx], -1, (255, 0, 0), 2)  # Blue color for the perimeter

    # Show the image with the simplified perimeter (for visual debugging)
    cv2.imshow('Less Approximate Green Object Perimeter', image)
    
    # Wait for a key press and close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return path  # Return the list of simplified contour points as the path


# Example usage:
perimeter_path = calculate_object_perimeter_path()
