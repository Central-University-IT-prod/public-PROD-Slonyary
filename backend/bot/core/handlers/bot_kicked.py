import asyncio

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ErrorEvent
from aiogram.utils.markdown import hbold

from core.utils.keyboards import ready_keyboard
from core.utils.messages import BotText


async def bot_removed(event: ErrorEvent):
    """
    Обработка чата, которым поделились
    """

    # user_id = event.update.message.chat.id
    # channel_id = event.update.message.chat_shared.chat_id

    try:
        msg = await event.update.message.answer("❌")
    except TelegramBadRequest:
        return

    await asyncio.sleep(1)

    try:
        await msg.delete()
    except TelegramBadRequest:
        pass

    await event.update.message.answer(
        text=BotText.bot_kicked.format(
            name=hbold(event.update.message.from_user.first_name)
        ),
        parse_mode="HTML",
        reply_markup=ready_keyboard,
    )
