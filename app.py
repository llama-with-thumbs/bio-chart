import time
from capture_image import capture_image
from firebase_uploader import upload_snippet_to_firebase
from rotate_image import rotate_image
from cut_and_save_snippet import cut_and_save_snippet
from upload_raw_image import upload_raw_image
from datetime import datetime
from calculate_mean_intensities import calculate_mean_intensities
from create_gif_from_images import create_gif_from_images
from upload_gif_file import upload_gif_file
from calculate_green_object_area import calculate_green_object_area

# Define the interval in seconds (30 minutes)
interval_seconds = 30 * 60  # 30 minutes * 60 seconds/minute

# Define the coordinates for cropping
# x, y, width, height
# coordinates_a = [1000, 450, 525, 730]
coordinates_b = [100, 100, 2392, 1820]

# Define the rotation angle
rotation_angle = 0  # Rotation angle in degrees

# Define chamber name
chamber = "CHA-146658"

# Define flasks names
flask_b = "SMP-96A579"

while True:
    # timestamp = datetime.now().isoformat()

    # image_path = capture_image(timestamp)

    # rotate_image(image_path, rotation_angle)

    # upload_raw_image(image_path, chamber, timestamp)

    # # Call the cut_and_save_rectangle function for each image
    # # snippet_path_a = cut_and_save_snippet(image_path, coordinates_a, flask_a, chamber)
    # snippet_path_b = cut_and_save_snippet(image_path, coordinates_b, flask_b, chamber)


    # # upload_snippet_to_firebase(snippet_path_a, flask_a, chamber, timestamp, calculate_mean_intensities(snippet_path_a), calculate_green_object_area(snippet_path_a))
    # upload_snippet_to_firebase(snippet_path_b, flask_b, chamber, timestamp, calculate_mean_intensities(snippet_path_b), calculate_green_object_area(snippet_path_b))

    # # create_gif_from_images(f"{chamber}/{flask_a}", f"{flask_a}.gif", 200, 0.1, 1)
    create_gif_from_images(f"{chamber}/{flask_b}", f"{flask_b}.gif", 200, 0.13, 2)

    
    # upload_gif_file(f"output_gif_folder/{flask_a}.gif", chamber, flask_a)
    upload_gif_file(f"output_gif_folder/{flask_b}.gif", chamber, flask_b)

   
    time.sleep(interval_seconds)
