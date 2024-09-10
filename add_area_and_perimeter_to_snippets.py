import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
from calculate_green_object_area import calculate_green_object_area
from calculate_object_perimeter_path import calculate_object_perimeter_path

chamber = "CHA-8BEA5D1"
flask = "SMP-9414B8"

def download_image(blob_path, local_directory="downloaded_images"):
    try:
        # Ensure local directory exists
        os.makedirs(local_directory, exist_ok=True)

        # Sanitize filename by replacing invalid characters
        filename = blob_path.split("/")[-1].replace(":", "_")

        # Create the full local path
        local_image_path = os.path.join(local_directory, filename)

        # Download image
        blob = storage.bucket().blob(blob_path)
        blob.download_to_filename(local_image_path)
        print(f"Downloaded {blob_path} to '{local_image_path}'")

        # Return the path to the downloaded image if successful
        return local_image_path
    
    except Exception as e:
        print(f"Error downloading image from {blob_path}: {e}")
        return None

def add_area_and_perimeter_to_snippets():
    try:
        # Initialize Firebase if not already done
        if not firebase_admin._apps:
            cred = credentials.Certificate("bio-chart-firebase.json")
            firebase_admin.initialize_app(cred, {"storageBucket": "bio-chart.appspot.com"})

        # Firestore reference
        db = firestore.client()
        snippets_ref = db.collection('bio-chart').document(chamber) \
            .collection('flasks').document(flask).collection('snippets')

        # Fetch and process documents
        for doc in snippets_ref.stream():
            data = doc.to_dict()
            if 'path' in data:
                local_image_path = download_image(data['path'])
                if local_image_path:
                    # Calculate green object area using the downloaded image
                    area = calculate_green_object_area(local_image_path)
                    perimeter_path = calculate_object_perimeter_path(local_image_path)
                    print(f"Calculated area: {area}")
                    print(f"Calculated perimeter path: {perimeter_path}")
                    
                    # Update the document with both calculated object_area and object_perimeter
                    snippets_ref.document(doc.id).update({
                        "object_area": area,
                        "object_perimeter": perimeter_path
                    })
                    print(f"Updated document {doc.id} with object_area: {area} and object_perimeter")
                else:
                    print(f"Failed to download image for document {doc.id}")
            else:
                print(f"Document {doc.id} has no 'path'")
    
    except Exception as e:
        print(f"Error processing snippets: {e}")

# Run the function
add_area_and_perimeter_to_snippets()
