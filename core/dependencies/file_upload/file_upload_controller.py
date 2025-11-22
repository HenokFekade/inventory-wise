from apps.file_upload.controllers.file_upload import FileUploadController

from apps.file_upload.services.cloudinary_file_upload import CloudinaryFileUploadService


def file_upload_controller_dep() -> FileUploadController:
    return FileUploadController(cloudinary_service=CloudinaryFileUploadService())
