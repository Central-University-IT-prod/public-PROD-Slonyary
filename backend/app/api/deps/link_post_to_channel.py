from typing import Annotated

import sqlalchemy as sa
from fastapi import Depends, HTTPException
from starlette import status

from app.api.deps import CrudTgChannelDepends, CrudVkChannelDepends, SessionDepends
from app.api.deps.universal import get_post_with_privileged_access
from app.crud import CrudTgChannel, CrudVkChannel
from app.schemas import Channel
from shared.core.enums import ChannelType
from shared.database.models import Post, PostsToTgChannels, PostsToVkChannels


async def _get_crud_and_model(
    channel_schema: Channel,
    tg_channel_crud: CrudTgChannel,
    vk_channel_crud: CrudVkChannel,
) -> tuple[CrudTgChannel | CrudVkChannel, type[PostsToTgChannels | PostsToVkChannels]]:
    if channel_schema.type == ChannelType.tg:
        crud = tg_channel_crud
        model = PostsToTgChannels
    elif channel_schema.type == ChannelType.vk:
        crud = vk_channel_crud
        model = PostsToVkChannels
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    channel = await crud.get(channel_schema.id)
    if channel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return crud, model


async def link_post_dep(
    post: Annotated[Post, Depends(get_post_with_privileged_access)],
    session: SessionDepends,
    channel_schema: Channel,
    tg_channel_crud: CrudTgChannelDepends,
    vk_channel_crud: CrudVkChannelDepends,
) -> None:
    crud, model = await _get_crud_and_model(
        channel_schema,
        tg_channel_crud,
        vk_channel_crud,
    )
    relation = model(post_id=post.id, channel_id=channel_schema.id)
    session.add(relation)
    await session.commit()


async def dislink_post_dep(
    post: Annotated[Post, Depends(get_post_with_privileged_access)],
    channel_schema: Channel,
    tg_channel_crud: CrudTgChannelDepends,
    vk_channel_crud: CrudVkChannelDepends,
    session: SessionDepends,
) -> None:
    crud, model = await _get_crud_and_model(
        channel_schema,
        tg_channel_crud,
        vk_channel_crud,
    )

    query = sa.delete(model).where(
        model.post_id == post.id,
        model.channel_id == channel_schema.id,
    )
    await session.execute(query)
    await session.commit()
