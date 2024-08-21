import asyncio
import logging

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from scheduler.utils.get_posts_to_publish import get_posts_to_publish
from shared.utils.publish_tg_post import publish_tg_post

# from shared.utils.publish_vk_post import publish_vk_post


async def post_publisher(
    bot: Bot,
    session: AsyncSession,
    interval: float = 60.0,
) -> None:
    logging.info("Старт цикла")
    while True:
        posts_to_publish = await get_posts_to_publish(session)
        logging.info(f"Получил {len(posts_to_publish)} постов на публикацию")

        for post in posts_to_publish:
            await publish_tg_post(post, bot, session)
            # await publish_vk_post(post)

        logging.info(f"Сон на {interval} секунд")
        await asyncio.sleep(interval)
