"""
Google Cloud Storage operations for handling audio files.
"""

import os
from typing import Optional

from google.cloud import storage


class GCSManager:
    """Manager for Google Cloud Storage operations."""

    def __init__(self, bucket_name: str):
        """
        Initialize the GCS manager.

        Args:
            bucket_name: Name of the Google Cloud Storage bucket
        """
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(bucket_name)

    def upload_file(
        self, source_file_path: str, destination_blob_name: Optional[str] = None
    ) -> str:
        """
        Upload a file to Google Cloud Storage.

        Args:
            source_file_path: Path to the local file to upload
            destination_blob_name: Name of the blob in GCS (defaults to file name)

        Returns:
            GCS URI of the uploaded file
        """
        if destination_blob_name is None:
            destination_blob_name = os.path.basename(source_file_path)

        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_path)

        return f"gs://{self.bucket_name}/{destination_blob_name}"

    def delete_file(self, blob_name: str) -> None:
        """
        Delete a file from Google Cloud Storage.

        Args:
            blob_name: Name of the blob to delete
        """
        blob = self.bucket.blob(blob_name)
        blob.delete()
