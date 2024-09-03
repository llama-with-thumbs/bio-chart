import time
from capture_image import capture_image
from firebase_uploader import upload_snippet_to_firebase
from rotate_image import rotate_image
from cut_and_save_snippet import cut_and_save_snippet
# from update_latest_image import update_latest_image
from upload_raw_image import upload_raw_image
from datetime import datetime
from calculate_mean_intensities import calculate_mean_intensities
from upload_gif_file import upload_gif_file

import os
import re

folder_path = "captured_images/C"

# Define the coordinates for cropping
# x, y, width, height
coordinates_b = [1200, 798, 425, 530]
coordinates_c = [1700, 868 ,425 ,530]

# Define the rotation angle
rotation_angle = 180  # Rotation angle in degrees

# Define chamber name
chamber = "CHA-8BEA5D1"

# Define flasks names
flask_b = "SMP-A0018B"
flask_c = "FLA-5B4CD"

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

    # do it only evey 12 houres.
    upload_gif_file(f"output_gif_folder/{flask_b}.gif", chamber, flask_b)
    upload_gif_file(f"output_gif_folder/{flask_c}.gif", chamber, flask_c)

    # # Call the cut_and_save_rectangle function for each image
    snippet_path_b = cut_and_save_snippet(image_path, coordinates_b, flask_b, chamber)
    snippet_path_c = cut_and_save_snippet(image_path, coordinates_c, flask_c, chamber)

    upload_snippet_to_firebase(snippet_path_b, flask_b, chamber, timestamp, calculate_mean_intensities(snippet_path_b))
    upload_snippet_to_firebase(snippet_path_c, flask_c, chamber, timestamp, calculate_mean_intensities(snippet_path_c))


    time.sleep(interval_seconds)
