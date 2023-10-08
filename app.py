import time
from capture_image import capture_image
from firebase_uploader import upload_image_to_firebase
from rotate_image import rotate_image
from cut_and_save_rectangle import cut_and_save_rectangle
from update_latest_image import update_latest_image

# Define the interval in seconds (10 minutes)
interval_seconds = 10 * 60  # 10 minutes * 60 seconds/minute

# Define the coordinates for cropping
width = 1000
height = 900
y=390

# Define the rotation angle
rotation_angle = -2.5  # Rotation angle in degrees

while True:
    # Capture an image and get its path
    image_path = capture_image()
    rotate_image(image_path, rotation_angle)

    # Call the cut_and_save_rectangle function for each image
    image_path_a = cut_and_save_rectangle(image_path, 800, y , width, height, "A_B")

    update_latest_image(image_path_a)

    upload_image_to_firebase(image_path_a, image_path_a)

    time.sleep(interval_seconds)
