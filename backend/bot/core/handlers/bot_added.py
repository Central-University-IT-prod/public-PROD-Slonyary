import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from core.settings.config import TOKEN
from core.utils.keyboards import reply_keyboard
from core.utils.messages import BotText

bot: Bot = Bot(TOKEN)


async def ready_handler(callback: CallbackQuery):
    """
    Обработка чата, которым поделились
    """

    try:
        msg = await callback.message.edit_text("✅")
    except TelegramBadRequest:
        msg = await callback.message.answer(
            text=BotText.ready_step.format(
                name=hbold(callback.message.from_user.first_name)
            ),
            parse_mode="HTML",
        )
    await asyncio.sleep(1)

    try:
        await msg.delete()
    except TelegramBadRequest:
        pass

    await callback.message.answer(
        text=BotText.ready_step.format(
            name=hbold(callback.message.from_user.first_name)
        ),
        parse_mode="HTML",
        reply_markup=reply_keyboard,
    )
