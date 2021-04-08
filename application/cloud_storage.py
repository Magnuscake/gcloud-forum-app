from google.cloud import storage

def upload_image(bucket_name, uploaded_image, destination_image_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"
#
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_image_name)

    blob.upload_from_string(
        uploaded_image.read(),
        content_type=uploaded_image.content_type
    )

