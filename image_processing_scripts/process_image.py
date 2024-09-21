import cv2
import numpy as np

# Import the functions from their respective scripts
from calculate_intersection_mask_and_area import calculate_intersection_mask_and_area
from calculate_object_perimeter_path import calculate_object_perimeter_path_from_mask
from calculate_object_perimeter_path import draw_polygon_from_path
from calculate_object_perimeter_path import show_polygon_on_image
from draw_polygon_from_json import draw_polygon_from_json

def process_image(image_path):
    print(image_path)
    # Step 1: Calculate the intersection mask and area
    intersected_mask, intersected_area = calculate_intersection_mask_and_area(image_path)
    
    # Step 2: Print the intersected area
    print(f"Intersected Area: {intersected_area} pixels")
    
    cv2.imshow("Intersected Mask again", intersected_mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Step 3: Calculate the perimeter path based on the intersection mask
    path, path_as_string = calculate_object_perimeter_path_from_mask(intersected_mask, image_path)
    
    # Step 4: Print the JSON string of the perimeter path
    print(f"Polygon perimeter path (JSON format): {path_as_string}")
    draw_polygon_from_path(path_as_string)
    # draw_polygon_from_json(path_as_string)
    # Step 5: Show the polygon on the original image
    show_polygon_on_image(image_path, path)

if __name__ == "__main__":
    # Example image path (modify this to the path of your image)
    image_path = 'test3.3.jpg'
    
    # Process the image
    process_image(image_path)
