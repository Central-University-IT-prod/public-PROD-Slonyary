from pydantic import Field

from shared.vk.entities.base import VkMethodInputParams


class SaveWallPhotoInput(VkMethodInputParams):
    user_id: int | None = None
    group_id: int | None = None
    photo: str
    server: int
    hash: str
    caption: str | None = Field(None, max_length=2048)
