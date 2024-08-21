import asyncio

from aiogram import Bot, Dispatcher, Router
from core.filters import ChatTypeFilter
from core.handlers import common
from core.middlewares.main import Middleware
from core.settings.commands import set_commands
from core.settings.config import TOKEN

# Базовые компоненты
bot: Bot = Bot(TOKEN)
dp: Dispatcher = Dispatcher()

main_router: Router = Router(name="main_router")
main_router.message.filter(ChatTypeFilter(chat_type="private"))


async def on_startup() -> None:
    """
    Вызывается при запуске бота
    """

    print("Бот запущен!")


async def on_closeup() -> None:
    """
    Вызывается при выключении бота
    """
    print("Бот отключен!")


async def main() -> None:
    # Регистрация обработчиков
    await common.register_main_handlers(main_router)

    # Установка команд бота для пользователей
    await set_commands(bot)

    # Dispatcher настройки
    dp.startup.register(on_startup)
    dp.include_router(main_router)

    # Регистрация Middlewares
    main_router.message.middleware(Middleware())

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        asyncio.get_event_loop().run_until_complete(on_closeup())
