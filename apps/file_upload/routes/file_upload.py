from fastapi import APIRouter, UploadFile, File, Depends

from apps.file_upload.controllers.file_upload import FileUploadController
from apps.file_upload.schemas.cloudinary_file_upload import FileUploadResponseSchema
from core.authentications.admin import admin_dep
from core.dependencies import file_upload_controller_dep

file_upload_router = APIRouter(prefix="/files/upload", tags=["File Upload"])


@file_upload_router.post("/account", response_model=FileUploadResponseSchema)
def upload_account(
        _=Depends(admin_dep),
        file: UploadFile = File(...),
        controller: FileUploadController = Depends(file_upload_controller_dep),
):
    return controller.upload_image(file=file, folder_name="accounts")


@file_upload_router.post("/category", response_model=FileUploadResponseSchema)
def upload_category(
        _=Depends(admin_dep),
        file: UploadFile = File(...),
        controller: FileUploadController = Depends(file_upload_controller_dep),
):
    return controller.upload_image(file=file, folder_name="categories")


@file_upload_router.post("/item", response_model=FileUploadResponseSchema)
def upload_item(
        _=Depends(admin_dep),
        file: UploadFile = File(...),
        controller: FileUploadController = Depends(file_upload_controller_dep),
):
    return controller.upload_image(file=file, folder_name="items")
