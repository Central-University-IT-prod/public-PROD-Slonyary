from aiogram.filters import BaseFilter
from aiogram.types import ErrorEvent


class BotKickedFilter(BaseFilter):
    def __init__(self):
        self.kicked_error = (
            "Telegram server says - Forbidden: bot was kicked from the channel chat"
        )

    async def __call__(self, event: ErrorEvent) -> bool:
        return str(event.exception) == self.kicked_error
