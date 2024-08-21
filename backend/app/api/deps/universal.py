from fastapi import HTTPException
from starlette import status

from app.api.deps import CrudPostDepends, CurrentUserDep
from shared.database.models import Post


async def get_post_with_privileged_access(
    post_id: int,
    user: CurrentUserDep,
    post_crud: CrudPostDepends,
) -> Post:
    post = await post_crud.get(post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not await post_crud.is_privileged_access(user.id, post):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return post


async def get_post_with_any_access(
    post_id: int,
    user: CurrentUserDep,
    post_crud: CrudPostDepends,
) -> Post:
    post = await post_crud.get(post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not await post_crud.is_user_access(user, post):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return post
