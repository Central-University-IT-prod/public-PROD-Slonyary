from aiogram.types import Message


async def message_handler(message: Message):
    """
    Обработка сообщений
    """

    await message.answer(text="⚡️ Напишите */start*", parse_mode="Markdown")
