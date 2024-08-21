from typing import Annotated

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import Depends

from shared.core.config import settings


def get_tg_bot() -> Bot:
    return Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(
            link_preview_is_disabled=True, parse_mode=ParseMode.HTML
        ),
    )


TgBotDepends = Annotated[Bot, Depends(get_tg_bot)]
