from shared.vk.entities.base import VkObject
from shared.vk.entities.size import Size


class Photo(VkObject):
    album_id: int
    date: int
    id: int
    owner_id: int
    access_key: str
    sizes: list[Size]
    text: str
    has_tags: bool
