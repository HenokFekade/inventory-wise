from typing import Optional, Any

from pydantic import BaseModel, AnyHttpUrl

from utils.schemas.base_schema import BaseResponseSchema


class CloudinaryUploadResponse(BaseModel):
    error_message: Optional[str] = None
    url: Optional[AnyHttpUrl] = None


class FileUploadSchema(BaseModel):
    url: AnyHttpUrl


class FileUploadResponseSchema(BaseResponseSchema):
    message: str = "File upload successfully"
    status: int = 200
    data: FileUploadSchema
