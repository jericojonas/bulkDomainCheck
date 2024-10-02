import firebase_admin
from firebase_admin import credentials, firestore
import os
import logging
from datetime import datetime
import pytz

# Initialize Firebase Admin SDK
cred = credentials.Certificate('serviceAccountKey.json')  # Replace with your service account key file path
firebase_admin.initialize_app(cred)

# Get a Firestore client
db = firestore.client()

def write_to_firestore(data):
    try:
        # Define the Firestore document reference
        doc_ref = db.collection('your collection name').document()

        # Write data to Firestore and get the document ID
        doc_ref.set(data)
        doc_id = doc_ref.id

        logging.info("Data successfully written to Firestore.")

        return doc_id
    except Exception as e:
        logging.error(f"Error writing data to Firestore: {e}")
        return None

if __name__ == "__main__":
    # Get current timestamp in Philippine Standard Time (PST)
    ph_timezone = pytz.timezone('Asia/Manila')
    current_time = datetime.now(ph_timezone)

    # Store result data
    result_data = {}

    # Iterate over all result files and extract data
    result_dir = 'result'
    for file_name in os.listdir(result_dir):
        if file_name.endswith('.txt'):
            file_path = os.path.join(result_dir, file_name)
            with open(file_path, 'r') as file:
                for line in file:
                    domain, status = line.strip().split(' - ')
                    result_data[domain] = status

    # Read the contents of "blocked.txt"
    summary = ""
    blocked_file_path = 'blocked.txt'
    if os.path.exists(blocked_file_path):
        with open(blocked_file_path, 'r') as blocked_file:
            summary = blocked_file.read()

    # Construct the document data
    doc_data = {
        'time': current_time,
        'result': result_data,
        'summary': summary  # Add the contents of "blocked.txt" to the document data
    }

    # Write document data to Firestore
    document_id = write_to_firestore(doc_data)

    # Save the document ID to "id.txt" file
    if document_id:
        with open('id.txt', 'w') as id_file:
            id_file.write(document_id)
