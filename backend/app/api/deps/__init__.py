from .crud import (
    CrudImageDepends,
    CrudPostDepends,
    CrudTgChannelDepends,
    CrudUserDepends,
    CrudUsersToTgChannelsDepends,
    CrudUsersToVkChannelsDepends,
    CrudVkChannelDepends,
)
from .current_user import CurrentUserDep
from .db import SessionDepends
from .tg_bot import TgBotDepends

__all__ = (
    "SessionDepends",
    "CrudImageDepends",
    "CrudTgChannelDepends",
    "CrudVkChannelDepends",
    "CrudPostDepends",
    "CrudUserDepends",
    "CurrentUserDep",
    "CrudUsersToTgChannelsDepends",
    "CrudUsersToVkChannelsDepends",
    "TgBotDepends",
)
