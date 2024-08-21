from shared.vk.entities.create_post import CreatePostInput, CreatePostOutput
from shared.vk.methods.base import VkBaseMethod


# https://dev.vk.com/ru/method/wall.post
class VkCreatePost(VkBaseMethod[CreatePostInput, CreatePostOutput]):
    __method__ = "wall.post"
    __input__ = CreatePostInput
    __output__ = CreatePostOutput
