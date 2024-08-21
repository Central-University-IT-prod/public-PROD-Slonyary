from aiogram import Bot
from aiogram.methods.set_my_commands import SetMyCommands
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram.types.bot_command import BotCommand

# Команды для пользователя
user_commands: list[BotCommand] = [
    BotCommand(command="start", description="Запуск"),
]


async def set_commands(bot: Bot) -> None:
    """
    Устанавливает команды для пользователей бота
    """

    await SetMyCommands(
        commands=user_commands, scope=BotCommandScopeAllPrivateChats()
    ).as_(bot)
