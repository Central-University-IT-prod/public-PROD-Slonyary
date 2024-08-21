from io import BytesIO

from shared.vk.entities.base import VkMethodOutputParams


class UploadPhotoInput(VkMethodOutputParams):
    upload_url: str
    filename: str
    photo: BytesIO


class UploadPhotoOutput(VkMethodOutputParams):
    server: int
    photo: str
    hash: str
