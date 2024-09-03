import time
from capture_image import capture_image
from firebase_uploader import upload_snippet_to_firebase
from rotate_image import rotate_image
from cut_and_save_snippet import cut_and_save_snippet
# from update_latest_image import update_latest_image
from upload_raw_image import upload_raw_image
from datetime import datetime
from calculate_mean_intensities import calculate_mean_intensities
from create_gif_from_images import create_gif_from_images
from upload_gif_file import upload_gif_file

# Define the interval in seconds (30 minutes)
interval_seconds = 30 * 60  # 30 minutes * 60 seconds/minute

# Define the coordinates for cropping
# x, y, width, height
coordinates_b = [500, 150, 525, 760]
coordinates_c = [1350, 150 ,525, 760]

# Define the rotation angle
rotation_angle = -2.5  # Rotation angle in degrees

# Define chamber name
chamber = "CHA-18E9A6"

# Define flasks names
flask_b = "SMP-388D43"
flask_c = "SMP-12D189"

while True:
    # Capture an image and get its path
    timestamp = datetime.now().isoformat()

    image_path = capture_image(timestamp)

    rotate_image(image_path, rotation_angle)

    upload_raw_image(image_path, chamber, timestamp)

    # do it only evey 12 houres.
    create_gif_from_images(f"{chamber}/{flask_b}", f"{flask_b}.gif", 200, 0.1, 1)
    create_gif_from_images(f"{chamber}/{flask_c}", f"{flask_c}.gif", 200, 0.1, 1)
    upload_gif_file(f"output_gif_folder/{flask_c}.gif", chamber, flask_c)
    upload_gif_file(f"output_gif_folder/{flask_b}.gif", chamber, flask_b)

    # # Call the cut_and_save_rectangle function for each image
    snippet_path_b = cut_and_save_snippet(image_path, coordinates_b, flask_b, chamber)
    snippet_path_c = cut_and_save_snippet(image_path, coordinates_c, flask_c, chamber)

    upload_snippet_to_firebase(snippet_path_b, flask_b, chamber, timestamp, calculate_mean_intensities(snippet_path_b))
    upload_snippet_to_firebase(snippet_path_c, flask_c, chamber, timestamp, calculate_mean_intensities(snippet_path_c))


    time.sleep(interval_seconds)
