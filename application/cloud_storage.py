import os
from google.cloud import storage

storage_client = storage.Client()

def upload_image(bucket_name, uploaded_image, destination_image_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"
#
    bucket = storage_client.get_bucket(bucket_name)
    _, file_ext = os.path.splitext(uploaded_image.filename)
    blob = bucket.blob(f"{destination_image_name}{file_ext}")

    blob.upload_from_string(
        uploaded_image.read(),
        content_type=uploaded_image.content_type
    )

    return blob.name

def make_blob_public(bucket_name, image_name):
    bucket = storage_client.get_bucket(bucket_name)

    file_ext = [".png", ".jpg", ".jpeg", ".webp"]

    for ext in file_ext:
        image_blob = bucket.blob(f"{image_name}{ext}")
        if image_blob.exists():
            image_blob.make_public()

def retrive_image(bucket_name, image_name):
    bucket = storage_client.get_bucket(bucket_name)

    blob_public_url = f"https://storage.googleapis.com/{bucket.id}/"

    file_ext = [".png", ".jpg", ".jpeg", ".webp"]

    for ext in file_ext:
        image_blob = bucket.blob(f"{image_name}{ext}")
        if image_blob.exists():
            return f"{blob_public_url}{image_blob.name}"

    return None

