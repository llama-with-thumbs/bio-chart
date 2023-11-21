import time
from capture_image import capture_image
from firebase_uploader import upload_snippet_to_firebase
from rotate_image import rotate_image
from cut_and_save_snippet import cut_and_save_snippet
# from update_latest_image import update_latest_image
from upload_raw_image import upload_raw_image
from datetime import datetime
from calculate_mean_intensities import calculate_mean_intensities

import os
import re

folder_path = "captured_images/C"

# Define the coordinates for cropping
# x, y, width, height
coordinates_a = [410, 868, 425, 530]
coordinates_b = [1060, 868 ,425 ,530]
coordinates_c = [1700, 868 ,425 ,530]

# Define the rotation angle
rotation_angle = 0  # Rotation angle in degrees

# Define chamber name
chamber = "CHA-18E9A6"

# Define flasks names
flask_a = "FLA-99606"
flask_b = "FLA-6A7F0"
flask_c = "FLA-5B4CD"
file_date_pairs = []  # List to store date-time and file path pairs

# Define the regular expression pattern to match the date
pattern = re.compile(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}")

# Iterate through the folder
for root, dirs, files in os.walk(folder_path):
    for file_name in files:
        file_path = os.path.join(root, file_name)

        # Find the match in the filename
        match = pattern.search(file_name)
        if match:
            date_str = match.group()
            date_time_obj = datetime.strptime(date_str, "%Y-%m-%d_%H-%M-%S")

            # Append the pair to the list
            file_date_pairs.append((date_time_obj, file_path))

# Sort the pairs based on time
file_date_pairs.sort(key=lambda pair: pair[0])

# Print sorted pairs
for i, (date_time_obj, file_path) in enumerate(file_date_pairs, start=1):
    if i % 40 == 0:
        iso_format_date = date_time_obj.isoformat()
        print(f"Path of the {i}th file: {file_path}, ISO Format Date: {iso_format_date}")
        upload_snippet_to_firebase(file_path, flask_c, chamber, iso_format_date, calculate_mean_intensities(file_path))

# while True:
#     # Capture an image and get its path
#     timestamp = datetime.now().isoformat()

#     image_path = capture_image(timestamp)

#     rotate_image(image_path, rotation_angle)

#     upload_raw_image(image_path, chamber, timestamp)

#     # # Call the cut_and_save_rectangle function for each image
#     snippet_path_a = cut_and_save_snippet(image_path, coordinates_a, flask_a, chamber)
#     snippet_path_b = cut_and_save_snippet(image_path, coordinates_b, flask_b, chamber)
#     snippet_path_c = cut_and_save_snippet(image_path, coordinates_c, flask_c, chamber)

#     # update_latest_image(image_path_a)
#     # update_latest_image(image_path_b)
#     # update_latest_image(image_path_c)

#     upload_snippet_to_firebase(snippet_path_a, flask_a, chamber, timestamp, calculate_mean_intensities(snippet_path_a))
#     upload_snippet_to_firebase(snippet_path_b, flask_b, chamber, timestamp, calculate_mean_intensities(snippet_path_b))
#     upload_snippet_to_firebase(snippet_path_c, flask_c, chamber, timestamp, calculate_mean_intensities(snippet_path_c))

