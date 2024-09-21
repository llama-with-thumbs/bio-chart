import cv2
import numpy as np
import json

def calculate_object_perimeter_path_from_mask(intersection_mask, original_image_path, epsilon_factor=0.002):
    # Read the original image to get its dimensions
    image = cv2.imread(original_image_path)
    height, width, _ = image.shape  # Get the dimensions of the image

    # Define the four corners of the original image
    image_frame = [
        [0, 0],  # Top-left
        [width - 1, 0],  # Top-right
        [width - 1, height - 1],  # Bottom-right
        [0, height - 1]  # Bottom-left
    ]

    # Find contours in the intersection mask
    contours, _ = cv2.findContours(intersection_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    path = []

    # Approximate the contours to reduce the number of points
    for contour in contours:
        epsilon = epsilon_factor * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        for point in approx:
            x, y = point[0]
            path.append([int(x), int(y)])  # Add contour points to path

    # Combine the image frame (corners) with the calculated path
    full_path = image_frame + path

    # Convert the path to a JSON string
    path_as_string = json.dumps(full_path)

    return full_path, path_as_string

def show_polygon_on_image(original_image_path, path):
    image = cv2.imread(original_image_path)

    # Ensure the path has at least 4 points for the image size
    if len(path) < 4:
        raise ValueError("Path should have at least 4 points for the corners.")

    # Extract the first four points as the image corners (top-left, top-right, bottom-right, bottom-left)
    top_left = path[0]
    top_right = path[1]
    bottom_right = path[2]
    bottom_left = path[3]

    # Calculate width and height based on the corners
    width = top_right[0] - top_left[0]
    height = bottom_left[1] - top_left[1]

    # Ensure the image matches the bounding box size
    resized_image = cv2.resize(image, (width, height))

    # The rest of the points in the path (after the first four) are the polygon to be drawn
    polygon_points = np.array(path[4:], dtype=np.int32)

    if len(polygon_points) > 0:
        # Draw the polygon on the resized image
        cv2.polylines(resized_image, [polygon_points], isClosed=True, color=(0, 255, 0), thickness=2)

        # Draw points on the polygon
        for point in polygon_points:
            cv2.circle(resized_image, tuple(point), radius=5, color=(0, 0, 255), thickness=-1)  # Red circles for each point

    # Display the resized image with the drawn polygon and points
    cv2.imshow("Polygon with Points", resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def draw_polygon_from_path(path_as_string):
    try:
        # Parse the path string into a list of points
        path = json.loads(path_as_string)

        # Extract the first four points as window corners (bounding box)
        top_left = path[0]
        top_right = path[1]
        bottom_right = path[2]
        bottom_left = path[3]

        # Calculate the width and height of the window based on these four points
        width = top_right[0] - top_left[0]
        height = bottom_left[1] - top_left[1]

        # Create a blank image (window) based on the size
        window = np.zeros((height, width, 3), dtype=np.uint8)

        # Extract the polygon points (exclude the first four points used for the bounding box)
        polygon_points = np.array(path[4:], dtype=np.int32)

        # Shift the polygon points to fit within the window
        # This ensures that the polygon is drawn within the (0,0) to (width, height) range
        shifted_polygon_points = polygon_points - [top_left[0], top_left[1]]

        # Draw the polygon on the window
        cv2.polylines(window, [shifted_polygon_points], isClosed=True, color=(0, 255, 0), thickness=2)

        # Draw points on the polygon
        for point in shifted_polygon_points:
            cv2.circle(window, tuple(point), radius=5, color=(0, 0, 255), thickness=-1)

        # Show the window with the drawn polygon
        cv2.imshow("Polygon on Window", window)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except json.JSONDecodeError:
        print("Invalid JSON format for path.")
    except Exception as e:
        print(f"Error occurred: {e}")
