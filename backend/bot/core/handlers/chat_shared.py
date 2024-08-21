import asyncio
import os
import traceback

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from core.handlers.logger import TgLogger
from core.services.database import add_channel, get_channel_by_id
from core.services.functions import image_to_base64
from core.settings.config import TOKEN
from core.utils.keyboards import ready_keyboard, return_keyboard
from core.utils.messages import BotText
from sqlalchemy.ext.asyncio import AsyncSession

tg_log = TgLogger()
bot: Bot = Bot(TOKEN)


async def folder_clean(file_path: str):
    try:
        for filename in os.listdir(file_path):
            file_path = os.path.join(file_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception:
                print(traceback.format_exc())
    except Exception:
        print(traceback.format_exc())


async def shared_handler(message: Message, session: AsyncSession):
    """
    Обработка чата, которым поделились
    """

    try:
        await message.delete()
    except TelegramBadRequest:
        pass

    chat_shared_id: int = message.chat_shared.chat_id
    channel = await get_channel_by_id(chat_shared_id)

    if channel:
        await message.answer(BotText.channel_already_added, parse_mode="HTML")
        return

    try:
        chat_info = await bot.get_chat(chat_id=chat_shared_id)
    except TelegramBadRequest:
        msg = await message.answer("❌")
        await asyncio.sleep(1)

        try:
            await msg.delete()
        except TelegramBadRequest:
            pass

        await message.answer(
            text=BotText.bot_kicked, parse_mode="HTML", reply_markup=ready_keyboard
        )
        return

    msg = await message.answer("🎉")
    await asyncio.sleep(1.7)

    try:
        await msg.delete()
    except TelegramBadRequest:
        pass

    await message.answer(
        text=BotText.added_channel, parse_mode="HTML", reply_markup=return_keyboard
    )

    username = "@" + chat_info.username if chat_info.username else None

    if not username:
        username = await bot.create_chat_invite_link(
            chat_id=chat_shared_id, name="Служебная ссылка"
        )
        username = username.invite_link

    try:
        subscribers = await bot.get_chat_member_count(chat_shared_id)
    except Exception:
        subscribers = 0

    image = None

    destination = "media/profile_photo/"
    file_name = f"/{message.chat.id}_{message.message_id}.png"

    try:
        os.mkdir(destination)
    except FileExistsError:
        pass

    try:
        if chat_info.photo:
            photo = chat_info.photo

            await bot.download(
                file=photo.file_id, destination=destination + file_name, seek=False
            )

            image = await image_to_base64(destination + file_name)
    except Exception:
        print(traceback.format_exc())
    finally:
        await folder_clean(destination)

    print(f"Канал {chat_info.title} добавлен")

    await add_channel(
        session=session,
        channel_id=chat_info.id,
        owner_id=message.from_user.id,
        title=chat_info.title,
        subscribers=subscribers,
        description=chat_info.description,
        username=username,
        photo_base64=image,
    )

    await tg_log.message(text=f"Канал {chat_info.title} добавлен")
