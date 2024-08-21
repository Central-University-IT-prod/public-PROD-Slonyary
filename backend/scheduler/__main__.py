import asyncio
import contextlib
import logging
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import close_all_sessions

from scheduler.tasks.publish import post_publisher
from shared.core.config import settings
from shared.database.session import db_session_manager


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True,
        ),
    )
    async with bot.context():
        async with db_session_manager() as session:
            try:
                await post_publisher(bot, session, interval=60)
            finally:
                await close_all_sessions()


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
