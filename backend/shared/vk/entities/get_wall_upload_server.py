from shared.vk.entities.base import VkMethodInputParams, VkMethodOutputParams


class GetWallUploadServerInput(VkMethodInputParams):
    group_id: int


class GetWallUploadServerOutput(VkMethodOutputParams):
    album_id: int
    upload_url: str
    user_id: int
