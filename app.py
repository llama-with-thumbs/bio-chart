import time
from capture_image import capture_image
from firebase_uploader import upload_snippet_to_firebase
from rotate_image import rotate_image
from cut_and_save_snippet import cut_and_save_snippet
# from update_latest_image import update_latest_image
from upload_raw_image import upload_raw_image
from datetime import datetime
from calculate_mean_intensities import calculate_mean_intensities

# Define the interval in seconds (30 minutes)
interval_seconds = 30 * 60  # 30 minutes * 60 seconds/minute

# Define the coordinates for cropping
# x, y, width, height
coordinates_a = [410, 868, 425, 530]
coordinates_b = [1060, 868 ,425 ,530]
coordinates_c = [1700, 868 ,425 ,530]

# Define the rotation angle
rotation_angle = 1.2  # Rotation angle in degrees

# Define chamber name
chamber = "CHA-AFBEFC"

# Define flasks names
flask_a = "SMP-8D8FDF"

while True:
    # Capture an image and get its path
    timestamp = datetime.now().isoformat()

    image_path = capture_image(timestamp)

    rotate_image(image_path, rotation_angle)

    upload_raw_image(image_path, chamber, timestamp)

    # # Call the cut_and_save_rectangle function for each image
    snippet_path_a = cut_and_save_snippet(image_path, coordinates_a, flask_a, chamber)

    # update_latest_image(image_path_a)
    # update_latest_image(image_path_b)
    # update_latest_image(image_path_c)

    upload_snippet_to_firebase(snippet_path_a, flask_a, chamber, timestamp, calculate_mean_intensities(snippet_path_a))

    time.sleep(interval_seconds)
