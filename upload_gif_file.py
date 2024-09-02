import os
import firebase_admin
from firebase_admin import credentials, storage, firestore

def upload_gif_file(gif_path,  chamber, flask):
    # Initialize Firebase Admin SDK with credentials
    cred = credentials.Certificate("bio-chart-firebase.json")
    firebase_admin.initialize_app(cred, {"storageBucket": "bio-chart.appspot.com"})

    # Extract the file name from the gif_path
    file_name = os.path.basename(gif_path)

    # Define the category and updated firebase_gif_path
    category = "output_gif_folder"
    firebase_gif_path = f"{category}/{file_name}"

    # Reference to the Firebase Storage bucket
    bucket = storage.bucket()

    # Upload the GIF to Firebase Storage
    blob = bucket.blob(firebase_gif_path.replace("\\", "/"))
    blob.upload_from_filename(gif_path.replace("\\", "/"), content_type="image/gif")

    print(f"GIF uploaded to Firebase Storage at '{firebase_gif_path}'")

    # Create a Firestore client
    db = firestore.client()

    # Add the new document to the specified collection
    flask_doc_ref = db.collection('bio-chart').document(chamber).collection('flasks').document(flask)

    flask_doc_ref.update({
        'gif_path': firebase_gif_path
    })

    print("Document added successfully.")

    # End the Firebase session
    firebase_admin.delete_app(firebase_admin.get_app())