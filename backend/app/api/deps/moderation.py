from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from app.api.deps import CrudPostDepends, SessionDepends, TgBotDepends
from app.api.deps.universal import get_post_with_privileged_access
from shared.core.enums import PostStatus
from shared.database.models import Post
from shared.utils.publish_tg_post import notify_owner_about_publish, publish_tg_post


async def accept_post_dep(
    post: Annotated[Post, Depends(get_post_with_privileged_access)],
    session: SessionDepends,
) -> Post:
    post.status = PostStatus.pending
    await session.commit()
    return post


async def reject_post_dep(
    post: Annotated[Post, Depends(get_post_with_privileged_access)],
    crud_posts: CrudPostDepends,
) -> Post:
    await crud_posts.delete(post.id)
    return post


async def downgrade_post_dep(
    session: SessionDepends,
    post: Annotated[Post, Depends(get_post_with_privileged_access)],
) -> Post:
    if post.status != PostStatus.pending:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    post.status = PostStatus.moderation
    await session.commit()

    return post


async def publish_post_dep(
    session: SessionDepends,
    bot: TgBotDepends,
    post: Annotated[Post, Depends(get_post_with_privileged_access)],
) -> Post:
    if post.status == PostStatus.published:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    await publish_tg_post(post, bot, session)
    await session.commit()
    await notify_owner_about_publish(post, bot)

    return post
