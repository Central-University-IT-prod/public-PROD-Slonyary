from typing import cast

from fastapi import APIRouter, HTTPException

from app.api.deps import (
    CrudTgChannelDepends,
    CrudUsersToTgChannelsDepends,
    CrudUsersToVkChannelsDepends,
    CrudVkChannelDepends,
    CurrentUserDep,
)
from app.schemas import (
    PreviewTgChannel,
    PreviewVkChannel,
    Result,
    TgChannelMember,
    TgChannelRead,
    VkChannelMember,
    VkChannelRead,
)
from shared.core.enums import ChannelType
from shared.database.models import TgChannel, User

router = APIRouter(prefix="/channels", tags=["channels"])


def get_posts_on_moderation(channel: TgChannel) -> int:
    r = 0
    for post in channel.posts:
        r += post.status == "moderation"
    return r


def get_posts_on_pending(channel: TgChannel) -> int:
    r = 0
    for post in channel.posts:
        r += post.status == "pending"
    return r


@router.get("/{type}", status_code=200)
async def get_channels(type: str, user: CurrentUserDep) -> list[PreviewTgChannel]:
    if type == ChannelType.tg:
        channels = user.tg_channels
        preview = PreviewTgChannel
    elif type == ChannelType.vk:
        channels = user.vk_channels
        preview = PreviewVkChannel
    else:
        raise HTTPException(404)

    return [
        preview(
            id=channel.id,
            photo_url=channel.photo_base64,
            name=channel.title,
            username=channel.username,
            subscribers=channel.subscribers,
            type=type,
            on_moderation=get_posts_on_moderation(channel),
            on_pending=get_posts_on_pending(channel),
        )
        for channel in channels
    ]


@router.get("/{type}/{post_id}")
async def get_channel(
    type: str,
    post_id: int,
    user: CurrentUserDep,
    crud_tg_channel: CrudTgChannelDepends,
    crud_user_to_tg_channel: CrudUsersToTgChannelsDepends,
    crud_vk_channel: CrudVkChannelDepends,
    crud_user_to_vk_channel: CrudUsersToVkChannelsDepends,
) -> TgChannelRead:
    if type == ChannelType.tg:
        crud = crud_tg_channel
        relation_crud = crud_user_to_tg_channel
        member = TgChannelMember
        read = TgChannelRead
    elif type == ChannelType.vk:
        crud = crud_vk_channel
        relation_crud = crud_user_to_vk_channel
        member = VkChannelMember
        read = VkChannelRead
    else:
        raise HTTPException(404)

    channel = await crud.get(post_id)
    if channel is None:
        raise HTTPException(404, detail="Not found")

    if not await relation_crud.is_user_access(user, channel):
        raise HTTPException(404, detail="Not found")

    workers = []
    for user in cast(list[User], channel.users):
        relation = await relation_crud.get_relation(user.id, channel.id)
        workers.append(
            member(
                user_id=user.id,
                role=relation.role,
                name=user.name,
                photo_url=user.photo_url,
            )
        )
    return read(
        id=channel.id,
        photo_url=channel.photo_base64,
        name=channel.title,
        username=channel.username,
        subscribers=channel.subscribers,
        description=channel.description,
        workers=workers,
        type=ChannelType.tg,
        owner_id=channel.owner_id,
    )


@router.delete("/{type}/{post_id}", status_code=200)
async def delete_channel(
    type: str,
    post_id: int,
    user: CurrentUserDep,
    crud_tg_channel: CrudTgChannelDepends,
    crud_vk_channel: CrudVkChannelDepends,
) -> Result:
    if type == ChannelType.tg:
        tg_channel = await crud_tg_channel.get(post_id)

        if not tg_channel or tg_channel.owner_id != user.id:
            raise HTTPException(404)

        await crud_tg_channel.delete(tg_channel.id)
        return Result(status="ok")

    elif type == ChannelType.vk:
        vk_channel = await crud_vk_channel.get(post_id)

        if not vk_channel or vk_channel.owner_id != user.id:
            raise HTTPException(404)

        await crud_vk_channel.delete(vk_channel.id)
        return Result(status="ok")

    else:
        raise HTTPException(404)


@router.delete("/{type}/{post_id}/{user_id}", status_code=200)
async def delete_user_from_channel(
    type: str,
    post_id: int,
    user_id: int,
    user: CurrentUserDep,
    crud_tg_channel: CrudTgChannelDepends,
    crud_vk_channel: CrudVkChannelDepends,
    crud_users_to_tg_channels: CrudUsersToTgChannelsDepends,
    crud_users_to_vk_channels: CrudUsersToVkChannelsDepends,
) -> Result:
    if type == ChannelType.tg:
        tg_channel = await crud_tg_channel.get(post_id)

        if not tg_channel or tg_channel.owner_id != user.id:
            raise HTTPException(404, detail="Не найдено")

        if user_id == tg_channel.owner_id:
            raise HTTPException(403, detail="Нельзя удалить самого себя")

        await crud_users_to_tg_channels.delete_relation(user_id, post_id)
        return Result(status="ok")

    elif type == ChannelType.vk:
        vk_channel = await crud_vk_channel.get(post_id)

        if not vk_channel or vk_channel.owner_id != user.id:
            raise HTTPException(404, detail="Не найдено")

        if user_id == vk_channel.owner_id:
            raise HTTPException(403, detail="Нельзя удалить самого себя")

        await crud_users_to_vk_channels.delete_relation(user_id, post_id)
        return Result(status="ok")

    else:
        raise HTTPException(404)
