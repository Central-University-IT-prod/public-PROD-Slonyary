from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonRequestChat,
    ReplyKeyboardMarkup,
)


class SimpleCallback(CallbackData, prefix="btn"):
    action: str


reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="Добавить канал",
                request_chat=KeyboardButtonRequestChat(
                    request_id=1,
                    chat_is_channel=True,
                    bot_is_member=True,
                ),
            )
        ]
    ],
    is_persistent=True,
    resize_keyboard=True,
)

ready_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Готово", callback_data="btn:ready")]
    ]
)

return_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Вернуться на сайт", url="http://prod.zzentqgpt.ru/channels"
            )
        ]
    ]
)

open_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Перейти сайт", url="http://prod.zzentqgpt.ru/channels"
            )
        ]
    ]
)
