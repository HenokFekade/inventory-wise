from fastapi import UploadFile

from apps.file_upload.schemas.cloudinary_file_upload import FileUploadResponseSchema
from apps.file_upload.services.cloudinary_file_upload import CloudinaryFileUploadService
from exceptions.bad_request import BadRequestException


class FileUploadController:
    def __init__(self, cloudinary_service: CloudinaryFileUploadService):
        self._cloudinary_service = cloudinary_service

    def upload_image(self, file: UploadFile, folder_name: str) -> FileUploadResponseSchema:
        # check if file is image type
        content_types = [
            "image/jpeg",
            "image/jpg",
            "image/png",
            "image/gif",
            "image/bmp",
            "image/webp",
            "image/tiff",
            "image/tif",
            "image/svg+xml",
            "image/x-icon",
            "image/heic",
            "image/heif",
            "image/avif",
        ]
        if file.content_type not in content_types:
            BadRequestException.throw("file should be image type")
        if file.size == 0:
            BadRequestException.throw("file size should be >= 0kb")
        response = self._cloudinary_service.upload(folder_name=f"inventory-wise/{folder_name}", image=file)
        if response.error_message:
            BadRequestException.throw(response.error_message)
        return FileUploadResponseSchema(data={"url": response.url})
