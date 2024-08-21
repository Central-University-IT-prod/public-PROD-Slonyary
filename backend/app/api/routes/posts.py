from fastapi import APIRouter, HTTPException
from starlette import status

from app.api.deps import CrudPostDepends, CurrentUserDep, SessionDepends
from app.schemas import ImageRead, PostCreate, PostIn, PostUpdate, PreviewPost, Result
from app.schemas.posts import PostChannel
from shared.core.enums import ChannelType, PostStatus
from shared.database.models import Post, PostsToTgChannels, PostsToVkChannels, User

router = APIRouter(prefix="/posts", tags=["posts"])


async def get_post_preview(post: Post, user: User) -> PreviewPost:
    channels = []
    for tg_channel in post.tg_channels:
        channels.append(
            PostChannel(
                id=tg_channel.id,
                name=tg_channel.title,
                subscribers=tg_channel.subscribers,
                avatar=tg_channel.photo_base64,
                type="tg",
            )
        )
    for vk_channel in post.vk_channels:
        channels.append(
            PostChannel(
                id=vk_channel.id,
                name=vk_channel.title,
                subscribers=0,
                type="vk",
            )
        )
    return PreviewPost(
        id=post.id,
        status=post.status,
        channels=channels,
        publish_time=post.publish_time,
        owner_name=post.owner.name,
        html_text=post.html_text,
        plain_text=post.plain_text,
        is_owner=post.owner.id == user.id,
        photos=[ImageRead.model_validate(image) for image in post.images],
    )


@router.get("", status_code=status.HTTP_200_OK)
async def get_posts(
    user: CurrentUserDep,
    crud_post: CrudPostDepends,
) -> list[PreviewPost]:
    posts = await crud_post.get_user_posts(user)
    result = []

    for post in posts:
        post_preview = await get_post_preview(post, user)
        result.append(post_preview)

    return result


@router.post("", status_code=200)
async def create_post(
    user: CurrentUserDep,
    post_in: PostIn,
    crud_post: CrudPostDepends,
    db: SessionDepends,
) -> PreviewPost:
    user_channels = [(c.id, ChannelType.tg) for c in user.tg_channels] + [
        (c.id, ChannelType.vk) for c in user.vk_channels
    ]

    for channel in post_in.channels:
        if (channel.id, channel.type) not in user_channels:
            raise HTTPException(403, detail="Нет доступа")

    post_create = PostCreate(
        html_text=post_in.html_text,
        plain_text=post_in.plain_text,
        publish_time=post_in.publish_time,
        owner_id=user.id,
        status=PostStatus.moderation,
    )
    post = await crud_post.create(post_create)

    for channel in post_in.channels:
        if channel.type == ChannelType.tg:
            relation_model = PostsToTgChannels
        elif channel.type == ChannelType.vk:
            relation_model = PostsToVkChannels
        else:
            raise HTTPException(400, detail="wrong channel type")
        relation = relation_model(channel_id=channel.id, post_id=post.id)
        db.add(relation)

    await db.commit()

    return await get_post_preview(post, user)


@router.get("/{id}", status_code=200)
async def get_post(
    id: int,
    crud_post: CrudPostDepends,
    user: CurrentUserDep,
) -> PreviewPost:
    post = await crud_post.get(id)

    if not post:
        raise HTTPException(404, "Не найдено")

    if not await crud_post.is_user_access(user, post) and not post.owner_id == user.id:
        raise HTTPException(403, "Нет доступа")

    return await get_post_preview(post, user)


@router.delete("/{id}", status_code=202)
async def delete_post(
    id: int,
    crud_post: CrudPostDepends,
    user: CurrentUserDep,
) -> Result:
    post = await crud_post.get(id)
    if not post:
        raise HTTPException(404)

    if post.owner_id != user.id:
        raise HTTPException(403, "Нет доступа")

    await crud_post.delete(id)
    return Result(status="ok")


@router.patch("/{id}", status_code=200)
async def update_post(
    id: int,
    crud_post: CrudPostDepends,
    user: CurrentUserDep,
    post_update: PostUpdate,
) -> Result:
    post = await crud_post.get(id)

    if not post:
        raise HTTPException(404, "Не найдено")

    if not crud_post.is_user_access(user, post):
        raise HTTPException(403, "Нет доступа")

    await crud_post.update(post, post_update)
    return Result(status="ok")
