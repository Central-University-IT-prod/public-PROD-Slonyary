# Регистрация обработчиков
from aiogram import F, Router
from aiogram.filters import CommandStart

from ..filters import BotKickedFilter
from ..utils.keyboards import SimpleCallback
from .bot_added import ready_handler
from .bot_kicked import bot_removed
from .chat_shared import shared_handler
from .errors import error_handler
from .messages import message_handler
from .start import start_handler


async def register_main_handlers(router: Router) -> None:
    """
    Регистрация основных обработчиков
    """

    # Стартовая команда
    router.message.register(start_handler, CommandStart())
    router.message.register(shared_handler, F.chat_shared)
    router.message.register(message_handler)

    router.error.register(bot_removed, BotKickedFilter())
    router.errors.register(error_handler)

    router.callback_query.register(
        ready_handler, SimpleCallback.filter(F.action == "ready")
    )
