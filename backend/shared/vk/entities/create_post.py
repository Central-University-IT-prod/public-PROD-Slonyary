from shared.vk.entities.base import VkMethodInputParams, VkMethodOutputParams


class CreatePostInput(VkMethodInputParams):
    owner_id: int
    from_group: int = 1
    message: str | None
    attachments: str
    mark_as_ads: int = 0
    close_comments: int = 0
    mute_notifications: int = 0
    copyright: str | None = None


class CreatePostOutput(VkMethodOutputParams):
    post_id: int
