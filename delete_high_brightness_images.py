from PIL import Image, ImageStat
import os

def calculate_brightness(image_path):
    try:
        # Open the image using Pillow
        image = Image.open(image_path)

        # Convert the image to grayscale (L mode)
        gray_image = image.convert("L")

        # Calculate the brightness using the ImageStat module
        brightness_stat = ImageStat.Stat(gray_image)
        brightness = brightness_stat.mean[0]

        return brightness
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None

def delete_high_brightness_images(folder_path, threshold=100):
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print(f"The folder '{folder_path}' does not exist or is not a directory.")
        return

    # List all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    if not image_files:
        print(f"No image files found in '{folder_path}'.")
        return

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        brightness = calculate_brightness(image_path)

        if brightness is not None and brightness > threshold:
            os.remove(image_path)
            print(f"Deleted {image_file} (Brightness = {brightness:.2f})")

if __name__ == "__main__":
    folder_path = r"captured_images\A_B"
    delete_high_brightness_images(folder_path, threshold=100)
