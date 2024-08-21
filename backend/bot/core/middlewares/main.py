import os.path
import traceback
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from shared.database.models import User
from shared.database.session import db_session_manager
from core.handlers.logger import TgLogger
from core.services.functions import image_to_base64
from core.settings.config import TOKEN

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


class Middleware(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        async with db_session_manager() as session:
            query = select(User).where(User.id == event.from_user.id)
            user = await session.execute(query)
            user = user.scalar()
            print("here 1")

            if not user:
                image = None

                destination = "media/profile_photo/"
                file_name = f"/{event.chat.id}_{event.message_id}.png"

                try:
                    os.mkdir(destination)
                except FileExistsError:
                    pass

                photos = await event.from_user.get_profile_photos(offset=0, limit=1)

                try:
                    if photos.photos:
                        photo = photos.photos[0][-1]

                        await bot.download(
                            file=photo.file_id,
                            destination=destination + file_name,
                            seek=False,
                        )

                        image = await image_to_base64(destination + file_name)
                except Exception:
                    print(traceback.format_exc())
                finally:
                    await folder_clean(destination)

                user = (
                    insert(User)
                    .values(
                        id=event.from_user.id,
                        username=event.from_user.username,
                        name=event.from_user.first_name,
                        photo_url=image,
                    )
                    .returning(User)
                )

                user = await session.execute(user)
                try:
                    await session.commit()

                    user = user.scalar()

                    await tg_log.message(
                        text=f"Новый пользователь: {event.from_user.first_name}"
                    )
                    print(f"Новый пользователь: {event.from_user.first_name}")
                except IntegrityError:
                    user = None
                    await session.rollback()
                    print(traceback.format_exc())

            data["user"] = user
            data["session"] = session

            return await handler(event, data)
