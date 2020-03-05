
from google.cloud import storage
from google.oauth2 import service_account


def upload_blob():
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"
    credentials = service_account.Credentials.from_service_account_file("spamclogger-5dd55ad0a65c.json")
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket("spamclogger")
    blob = bucket.blob("wummington")

    print(blob.upload_from_filename("screenie.png"))

    print(
        "File {} uploaded to {}.".format(
            "screenie.png", "wummington"))

upload_blob()