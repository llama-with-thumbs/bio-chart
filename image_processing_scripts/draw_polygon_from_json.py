import cv2
import numpy as np
import json

def draw_polygon_from_json(json_data, image_size=(400, 400)):
    """
    Draws a polygon based on the given JSON of coordinates and displays the image.
    
    :param json_data: Serialized JSON string containing pairs of coordinates
    :param image_size: Size of the blank image (width, height)
    :return: None
    """

    # Parse JSON data into a list of coordinate pairs
    coordinates = json.loads(json_data)

    # Create a blank white image
    image = np.ones((image_size[1], image_size[0], 3), dtype=np.uint8) * 255

    # Convert the coordinates into a numpy array of shape (n, 1, 2) for OpenCV
    points = np.array(coordinates, np.int32).reshape((-1, 1, 2))

    # Draw the polygon
    cv2.polylines(image, [points], isClosed=True, color=(0, 255, 0), thickness=2)

    # Fill the polygon with a semi-transparent color (optional)
    cv2.fillPoly(image, [points], color=(179, 229, 252))  # Light blue fill

    # Display the image
    cv2.imshow('Polygon', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Example JSON data (coordinate pairs)
    json_coordinates = '[ [100, 150], [200, 80], [300, 150], [250, 250], [150, 250] ]'

    # Call the function to draw and display the image
    draw_polygon_from_json(json_coordinates)
