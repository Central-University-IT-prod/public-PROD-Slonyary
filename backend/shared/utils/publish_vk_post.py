import asyncio
import base64
from io import BytesIO
from typing import cast

import httpx

from shared.database.models import Image, Post, VkChannel
from shared.vk import VkBot
from shared.vk.entities.create_post import CreatePostOutput
from shared.vk.entities.photo import Photo


async def publish_vk_post(post: Post) -> None:
    tasks = []
    async with httpx.AsyncClient() as client:
        for channel in cast(list[VkChannel], post.vk_channels):
            tasks.append(asyncio.create_task(create_post(post, channel, client)))
        await asyncio.gather(*tasks)


async def create_post(
    post: Post,
    channel: VkChannel,
    client: httpx.AsyncClient,
) -> CreatePostOutput:
    bot = VkBot(channel.id, channel.access_token, client)
    photos = [await upload_image(bot, image) for image in post.images]
    return await bot.create_post(post.plain_text, photos)


async def upload_image(bot: VkBot, image: Image) -> Photo:
    upload_server = await bot.get_wall_upload_server()
    img_data = image.base64.encode()
    content = base64.b64decode(img_data)
    bytes_io = BytesIO(content)
    photo = await bot.upload_photo(bytes_io, image.filename, upload_server)
    saved_photos = await bot.save_photo(photo)
    return saved_photos[0]
