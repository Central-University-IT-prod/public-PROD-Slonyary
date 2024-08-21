import base64
from http.client import HTTPException
from typing import Annotated, cast

from fastapi import Depends, UploadFile

from app.api.deps import SessionDepends
from app.api.deps.universal import get_post_with_any_access
from shared.database.models import Image, Post


async def create_image_dep(
    file: UploadFile,
    post: Annotated[Post, Depends(get_post_with_any_access)],
    db: SessionDepends,
) -> Image:
    if len(post.images) >= 10:
        post.images = post.images[:10]
        await db.commit()
        raise HTTPException(409)

    b64 = base64.b64encode(await file.read()).decode()
    image_db = Image(post_id=post.id, filename=file.filename, base64=b64)
    db.add(image_db)
    await db.commit()
    return image_db


async def get_all_images_dep(
    post: Annotated[Post, Depends(get_post_with_any_access)],
) -> Image:
    return post.images


async def get_image_dep(
    image_id: int,
    post: Annotated[Post, Depends(get_post_with_any_access)],
) -> Image:
    for image in cast(list[Image], post.images):
        if image.id == image_id:
            return image
    raise HTTPException(404)


async def delete_image_dep(
    image_id: int,
    post: Annotated[Post, Depends(get_post_with_any_access)],
    db: SessionDepends,
) -> None:
    for image in cast(list[Image], post.images):
        if image.id == image_id:
            await db.delete(image)
            await db.commit()
            break
