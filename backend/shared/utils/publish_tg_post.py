import base64
import contextlib
import logging
from typing import cast

import sqlalchemy as sa
from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from aiogram.types import BufferedInputFile, InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from shared.core.enums import PostStatus
from shared.database.models import Image, Post, PostsToTgChannels, TgChannel


async def publish_tg_post(post: Post, bot: Bot, session: AsyncSession) -> None:
    media_group = await images_to_file_id_media(post, bot)
    text = post.html_text.replace("<p>", "").replace("</p>", "").replace("<br>", "")
    if media_group:
        logging.info(f"Отправка поста #{post.id} с медиагруппой")

        set_caption_to_media_group(text, media_group)
        for channel in cast(list[TgChannel], post.tg_channels):
            msgs = await bot.send_media_group(chat_id=channel.id, media=media_group)
            await link_post_message_id(post.id, channel.id, msgs[0].message_id, session)
    else:
        logging.info(f"Отправка поста #{post.id} без медиагруппы")

        for channel in cast(list[TgChannel], post.tg_channels):
            msg = await bot.send_message(chat_id=channel.id, text=text)
            await link_post_message_id(post.id, channel.id, msg.message_id, session)

    logging.info(f"Отправил пост #{post.id}")

    await mark_post_as_published(post, session)
    logging.info(f"Отметил пост #{post.id} опубликованным")

    await notify_owner_about_publish(post, bot)
    logging.info(f"Сообщил создателю поста #{post.id} о публикации")


async def images_to_file_id_media(post: Post, bot: Bot) -> list[InputMediaPhoto]:
    images = [image_to_media_photo(image) for image in post.images]
    if images:
        bot_messages = await bot.send_media_group(chat_id=post.owner_id, media=images)
        return [InputMediaPhoto(media=msg.photo[-1].file_id) for msg in bot_messages]
    return []


def image_to_media_photo(image: Image) -> InputMediaPhoto:
    img_data = image.base64.encode()
    content = base64.b64decode(img_data)
    media = BufferedInputFile(file=content, filename="filename")
    return InputMediaPhoto(media=media)


def set_caption_to_media_group(
    caption: str,
    media_group: list[InputMediaPhoto],
) -> None:
    media_group[0].caption = caption


async def link_post_message_id(
    post_id: int,
    channel_id: int,
    message_id: int,
    session: AsyncSession,
) -> None:
    query = (
        sa.update(PostsToTgChannels)
        .where(
            PostsToTgChannels.post_id == post_id,
            PostsToTgChannels.channel_id == channel_id,
        )
        .values(message_id=message_id)
    )
    await session.execute(query)
    await session.commit()


async def mark_post_as_published(post: Post, session: AsyncSession) -> None:
    post.status = PostStatus.published
    await session.commit()


async def notify_owner_about_publish(post: Post, bot: Bot) -> None:
    text = f"Пост #{post.id} опубликован!!!"
    with contextlib.suppress(TelegramAPIError):  # чтоб не сломалося
        await bot.send_message(chat_id=post.owner_id, text=text)
