import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CrudBase
from app.schemas import PostCreate, PostRead, PostUpdate
from shared.core.enums import UserChannelRole
from shared.database.models import (
    Post,
    PostsToTgChannels,
    TgChannel,
    User,
    UsersToTgChannels,
)


class CrudPost(CrudBase[Post, PostCreate, PostRead, PostUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Post)

    async def create(self, obj_in: PostCreate) -> Post:
        db_obj = Post(
            owner_id=obj_in.owner_id,
            html_text=obj_in.html_text,
            plain_text=obj_in.plain_text,
            publish_time=obj_in.publish_time,
            status=obj_in.status,
        )
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def is_user_access(self, user: User, post: Post) -> bool:
        if post.owner_id == user.id:
            return True

        query = sa.select(UsersToTgChannels).where(
            UsersToTgChannels.user_id == user.id,
            UsersToTgChannels.channel_id.in_(
                [c.id for c in post.tg_channels] + [c.id for c in post.vk_channels]
            ),
        )
        return bool(await self.db.scalar(query))

    async def is_privileged_access(self, user_id: int, post: Post) -> bool:
        if post.owner_id == user_id:
            return True

        query = sa.select(UsersToTgChannels.role).where(
            UsersToTgChannels.user_id == user_id,
            UsersToTgChannels.channel_id.in_([c.id for c in post.tg_channels]),
        )
        roles = await self.db.scalars(query)

        return roles and (
            UserChannelRole.owner in roles or UserChannelRole.moderator in roles
        )

    async def update(self, post: Post, post_update: PostUpdate) -> Post:
        """Updating post data."""
        if post_update.publish_time:
            post.publish_time = post_update.publish_time
        if post_update.html_text:
            post.html_text = post_update.html_text
        if post_update.plain_text:
            post.plain_text = post_update.plain_text

        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)
        return post

    async def get_user_posts(self, user: User) -> list[Post]:
        """Получение постов пользователя."""
        query = (
            sa.select(Post)
            .where(
                sa.or_(
                    Post.id.in_(
                        sa.select(PostsToTgChannels.post_id).where(
                            PostsToTgChannels.channel_id.in_(
                                sa.select(TgChannel.id).where(
                                    sa.or_(
                                        TgChannel.id.in_(
                                            sa.select(
                                                UsersToTgChannels.channel_id
                                            ).where(
                                                UsersToTgChannels.user_id == user.id
                                            )
                                        ),
                                        TgChannel.owner_id == user.id,
                                    )
                                )
                            )
                        )
                    ),
                    Post.owner_id == user.id,
                )
            )
            .order_by(Post.publish_time.desc(), Post.id.desc())
        )
        posts = list(await self.db.scalars(query))
        return posts
