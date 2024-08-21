from shared.vk.entities.get_wall_upload_server import (
    GetWallUploadServerInput,
    GetWallUploadServerOutput,
)
from shared.vk.methods.base import VkBaseMethod


# https://dev.vk.com/ru/method/photos.getWallUploadServer
class GetWallUploadServer(
    VkBaseMethod[
        GetWallUploadServerInput,
        GetWallUploadServerOutput,
    ]
):
    __method__ = "photos.getWallUploadServer"
    __input__ = GetWallUploadServerInput
    __output__ = GetWallUploadServerOutput
