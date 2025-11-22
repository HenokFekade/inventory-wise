import cloudinary
import cloudinary.uploader
from fastapi import UploadFile

from apps.file_upload.schemas.cloudinary_file_upload import CloudinaryUploadResponse
from core.config.config import config


class CloudinaryFileUploadService:
    @staticmethod
    def initialize():
        cloudinary.config(
            cloud_name=config.CLOUDINARY_NAME,
            api_key=config.CLOUDINARY_API_KEY,
            api_secret=config.CLOUDINARY_API_SECRET,
            secure=True
        )

    @staticmethod
    def upload(folder_name: str, image: UploadFile) -> CloudinaryUploadResponse:
        try:
            response: dict = cloudinary.uploader.upload(
                image.file,
                folder=f"{folder_name}",
                overwrite=True,
                resource_type="image",
            )
            url = response.get('secure_url')

            if url:
                return CloudinaryUploadResponse(url=url)
            return CloudinaryUploadResponse(error_message="Something went wrong during file uploading")
        except Exception as e:
            print("Something went wrong during file uploading", e)
            CloudinaryUploadResponse(error_message="Something went wrong during file uploading")
