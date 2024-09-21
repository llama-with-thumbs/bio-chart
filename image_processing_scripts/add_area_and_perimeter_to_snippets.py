import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
import numpy as np
from calculate_intersection_mask_and_area import calculate_intersection_mask_and_area
from calculate_object_perimeter_path import calculate_object_perimeter_path_from_mask
import cv2

chamber = "CHA-18E9A6"
flask = "SMP-12D189"

def download_image_if_needed(blob_path, local_directory=f"{flask}_downloaded_images"):
    try:
        os.makedirs(local_directory, exist_ok=True)
        filename = blob_path.split("/")[-1].replace(":", "_")
        local_image_path = os.path.join(local_directory, filename)

        # Check if the image already exists locally
        if os.path.exists(local_image_path):
            print(f"Image already exists locally: {local_image_path}")
            return local_image_path

        # Download image from Firebase Storage
        blob = storage.bucket().blob(blob_path)
        blob.download_to_filename(local_image_path)
        print(f"Downloaded {blob_path} to '{local_image_path}'")

        return local_image_path
    
    except Exception as e:
        print(f"Error downloading image from {blob_path}: {e}")
        return None

def add_area_and_perimeter_to_snippets():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate("../bio-chart-firebase.json")
            firebase_admin.initialize_app(cred, {"storageBucket": "bio-chart.appspot.com"})

        db = firestore.client()
        snippets_ref = db.collection('bio-chart').document(chamber) \
            .collection('flasks').document(flask).collection('snippets')

        for doc in snippets_ref.stream():
            data = doc.to_dict()
            if 'path' in data:
                # Check for image locally or download it if needed
                local_image_path = download_image_if_needed(data['path'])
                if local_image_path:
                    # Check if the image has been loaded correctly
                    image = cv2.imread(local_image_path)
                    if image is None:
                        print(f"Failed to load image: {local_image_path}")
                        continue  # Skip to the next snippet if image loading fails

                    # Calculate intersection mask and area
                    intersected_mask, intersected_area = calculate_intersection_mask_and_area(local_image_path)
                    
                    # Convert intersected_area from numpy type to standard Python int
                    intersected_area = int(intersected_area)
                    
                    # Calculate the perimeter path from the intersection mask
                    perimeter_path, path_as_string = calculate_object_perimeter_path_from_mask(intersected_mask, local_image_path)
                    
                    print(f"Calculated area: {intersected_area}")
                    
                    # Update Firestore document with standard Python types
                    snippets_ref.document(doc.id).update({
                        "object_area": intersected_area,
                        "object_perimeter": path_as_string
                    })
                    # print(f"Updated document {doc.id} with object_area: {intersected_area} and object_perimeter")
                else:
                    print(f"Failed to process image for document {doc.id}")
            else:
                print(f"Document {doc.id} has no 'path'")
    
    except Exception as e:
        print(f"Error processing snippets: {e}")

# Run the function
add_area_and_perimeter_to_snippets()
