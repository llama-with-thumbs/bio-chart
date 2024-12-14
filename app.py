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
interval_seconds = 10 * 60  # 30 minutes * 60 seconds/minute

# Define the coordinates for cropping
# x, y, width, height
coordinates_a = [530, 568, 425, 480]

# Define the rotation angle
rotation_angle = 1.5  # Rotation angle in degrees

# Define chamber name
chamber = "CHA-DDFBE6"

# Define flasks names
flask_a = "SMP-4FF31C"

while True:
    timestamp = datetime.now().isoformat()

    image_path = capture_image(timestamp)

    rotate_image(image_path, rotation_angle)

    upload_raw_image(image_path, chamber, timestamp)

    # # Call the cut_and_save_rectangle function for each image
    snippet_path_a = cut_and_save_snippet(image_path, coordinates_a, flask_a, chamber)

    upload_snippet_to_firebase(snippet_path_a, flask_a, chamber, timestamp, calculate_mean_intensities(snippet_path_a), calculate_green_object_area(snippet_path_a))
  
    create_gif_from_images(f"{chamber}/{flask_a}", f"{flask_a}.gif", 200, 0.1, 1)
    
    upload_gif_file(f"output_gif_folder/{flask_a}.gif", chamber, flask_a)
   
    time.sleep(interval_seconds)
