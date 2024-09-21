import cv2
import numpy as np

def get_brightness_mask(image_path):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    value_channel = hsv[:, :, 2]
    _, contrast_filtered = cv2.threshold(value_channel, 100, 255, cv2.THRESH_BINARY)
    blurred = cv2.GaussianBlur(contrast_filtered, (3, 3), 0)
    kernel = np.ones((10, 10), np.uint8)
    closed_mask = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel)
    flood_filled_mask = closed_mask.copy()
    h, w = flood_filled_mask.shape[:2]
    mask_floodfill = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(flood_filled_mask, mask_floodfill, (0, 0), 255)
    inverted_flood_fill = cv2.bitwise_not(flood_filled_mask)
    final_mask = cv2.bitwise_or(closed_mask, inverted_flood_fill)
    return final_mask

def get_green_mask(image_path):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([10, 60, 100])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    _, contrast_filtered = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)
    blurred = cv2.GaussianBlur(contrast_filtered, (3, 3), 0)
    kernel = np.ones((10, 10), np.uint8)
    closed_mask = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel)
    flood_filled_mask = closed_mask.copy()
    h, w = flood_filled_mask.shape[:2]
    mask_floodfill = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(flood_filled_mask, mask_floodfill, (0, 0), 255)
    inverted_flood_fill = cv2.bitwise_not(flood_filled_mask)
    final_mask = cv2.bitwise_or(closed_mask, inverted_flood_fill)
    return final_mask

def get_intersection_mask(image_path):
    brightness_mask = get_brightness_mask(image_path)
    green_mask = get_green_mask(image_path)
    intersected_mask = cv2.bitwise_and(brightness_mask, green_mask)
    
    # cv2.imshow("Intersected Mask", intersected_mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return brightness_mask

def calculate_intersection_mask_and_area(image_path):
    intersected_mask = get_intersection_mask(image_path)
    

    intersected_area = np.sum(intersected_mask > 0)  # Calculate the intersected area in pixels
    
    # print(f"Total intersected area: {intersected_area} pixels")
    
    return intersected_mask, intersected_area  # Return both the intersected mask and area
