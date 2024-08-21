from aiogram import Bot

from core.settings.config import TOKEN


class TgLogger:
    def __init__(self):
        self.chat_id: int = -1002110986870
        self.bot: Bot = Bot(TOKEN)

    async def message(self, text: str):
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=f"[MESSAGE]: {text}")
        except Exception:
            pass

    async def error(self, text: str):
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=f"[ERROR]: {text}")
        except Exception:
            pass
