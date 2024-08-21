from typing import Annotated

from fastapi import Depends

from app.api.deps.db import SessionDepends
from app.crud import (
    CrudImage,
    CrudPost,
    CrudTgChannel,
    CrudUser,
    CrudUsersToTgChannels,
    CrudUsersToVkChannels,
    CrudVkChannel,
)


def crud_user(db: SessionDepends) -> CrudUser:
    return CrudUser(db)


def crud_image(db: SessionDepends) -> CrudImage:
    return CrudImage(db)


def crud_tg_channel(db: SessionDepends) -> CrudTgChannel:
    return CrudTgChannel(db)


def crud_vk_channel(db: SessionDepends) -> CrudVkChannel:
    return CrudVkChannel(db)


def crud_post(db: SessionDepends) -> CrudPost:
    return CrudPost(db)


def crud_users_to_tg_channels(db: SessionDepends) -> CrudUsersToTgChannels:
    return CrudUsersToTgChannels(db)


def crud_users_to_vk_channels(db: SessionDepends) -> CrudUsersToVkChannels:
    return CrudUsersToVkChannels(db)


CrudImageDepends = Annotated[CrudImage, Depends(crud_image)]
CrudTgChannelDepends = Annotated[CrudTgChannel, Depends(crud_tg_channel)]
CrudVkChannelDepends = Annotated[CrudVkChannel, Depends(crud_vk_channel)]
CrudPostDepends = Annotated[CrudPost, Depends(crud_post)]
CrudUserDepends = Annotated[CrudUser, Depends(crud_user)]
CrudUsersToTgChannelsDepends = Annotated[
    CrudUsersToTgChannels, Depends(crud_users_to_tg_channels)
]
CrudUsersToVkChannelsDepends = Annotated[
    CrudUsersToVkChannels, Depends(crud_users_to_vk_channels)
]
