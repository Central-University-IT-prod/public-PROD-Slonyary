import asyncio
import traceback

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandObject
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from core.handlers.logger import TgLogger
from core.services.database import get_user, user_in_channel
from core.settings.config import TOKEN
from core.utils.keyboards import open_keyboard, ready_keyboard
from core.utils.messages import BotText
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.models import TgChannel, User, UsersToTgChannels

tg_log = TgLogger()
bot: Bot = Bot(TOKEN)


async def start_handler(
    message: Message,
    command: CommandObject,
    user: User,
    session: AsyncSession,
):
    """
    Команда /start
    """

    # Извлекаем данные переданные в команду
    deeplink = command.args

    if isinstance(deeplink, str) and deeplink.startswith("invite"):
        role_name = {"editor": "Редактором", "moderator": "Модератором"}

        channel_id, role = deeplink.replace("invite", "").split("_")

        if role not in ["editor", "moderator"]:
            await message.answer(
                text=BotText.error.format(
                    reason="Некорректная пригласительная ссылка - недопустимая роль"
                ),
                parse_mode="HTML",
            )
            return

        try:
            int(channel_id)
        except ValueError:
            await message.answer(
                text=BotText.error.format(reason="Некорректная пригласительная ссылка"),
                parse_mode="HTML",
            )
            return

        query = select(TgChannel).where(TgChannel.id == int(channel_id))
        channel = await session.execute(query)
        channel = channel.scalar()

        if not channel:
            await message.answer(
                text=BotText.error.format(
                    reason="Некорректная пригласительная ссылка - канал не найден"
                ),
                parse_mode="HTML",
            )
            return

        user_channel_link = await user_in_channel(
            session, message.from_user.id, channel.id
        )
        print(user_channel_link)

        if user_channel_link:
            if user_channel_link.role in [role, "owner"]:
                await message.answer(
                    text=BotText.error.format(
                        reason="Вы уже состоите в этом канале с этой ролью"
                    ),
                    parse_mode="HTML",
                )
                return
            else:
                query = (
                    update(UsersToTgChannels)
                    .values(
                        user_id=message.from_user.id, channel_id=channel.id, role=role
                    )
                    .where(
                        UsersToTgChannels.user_id == message.from_user.id,
                        UsersToTgChannels.channel_id == channel.id,
                    )
                    .returning(UsersToTgChannels.user_id)
                )
        else:
            query = (
                insert(UsersToTgChannels)
                .values(user_id=message.from_user.id, channel_id=channel.id, role=role)
                .returning(UsersToTgChannels.user_id)
            )

        await session.execute(query)

        try:
            await session.commit()
        except IntegrityError:
            print(traceback.format_exc())
            await session.rollback()
            await message.answer(
                text=BotText.error.format(reason="Ошибка при сохранение связи"),
                parse_mode="HTML",
            )
            return

        owner_user: User = await get_user(session, channel.owner_id)

        if not owner_user:
            await message.answer(
                text=BotText.error.format(reason="Ошибка при получении owner.id"),
                parse_mode="HTML",
            )
            return

        if user_channel_link and user_channel_link.role != role:
            await message.answer(
                text=BotText.edited_to_channel.format(
                    channel_title=channel.title,
                    owner_name=owner_user.name,
                    role_name=role_name[role],
                ),
                parse_mode="HTML",
                reply_markup=open_keyboard,
            )
        else:
            await message.answer(
                text=BotText.added_to_channel.format(
                    channel_title=channel.title,
                    owner_name=owner_user.name,
                    role_name=role_name[role],
                ),
                parse_mode="HTML",
                reply_markup=open_keyboard,
            )

        await tg_log.message(text="Создана связь")
        print("Создана связь")
        return

    msg = await message.answer("⚡")
    await asyncio.sleep(1)

    try:
        await msg.edit_text(
            text=BotText.start.format(name=hbold(message.from_user.first_name)),
            parse_mode="HTML",
            reply_markup=ready_keyboard,
        )
    except TelegramBadRequest:
        await message.answer(
            text=BotText.start.format(name=hbold(message.from_user.first_name)),
            parse_mode="HTML",
            reply_markup=ready_keyboard,
        )
