from typing import Literal

from shared.vk.entities.base import VkObject

MediaTypes = Literal[
    "photo",
    "video",
    "audio",
    "doc",
    "page",
    "note",
    "poll",
    "album",
    "market",
    "market_album",
    "audio_playlist",
]


class Media(VkObject):
    type: MediaTypes
    owner_id: int
    media_id: int | str

    def __str__(self) -> str:
        return f"{self.type}{self.owner_id}_{self.media_id}"
