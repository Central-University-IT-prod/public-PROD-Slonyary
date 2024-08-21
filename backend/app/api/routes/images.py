from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps.images import (
    create_image_dep,
    delete_image_dep,
    get_all_images_dep,
    get_image_dep,
)
from app.schemas import ImageRead, Result
from shared.database.models import Image

router = APIRouter(prefix="/posts/{post_id}/images", tags=["images"])


@router.get("", status_code=200)
async def get_all_images(
    images: Annotated[list[Image], Depends(get_all_images_dep)],
) -> list[ImageRead]:
    return [ImageRead.model_validate(image) for image in images]


@router.get("/{image_id}", status_code=200)
async def get_image(image: Annotated[Image, Depends(get_image_dep)]) -> ImageRead:
    return ImageRead.model_validate(image)


@router.post("", status_code=200)
async def create_image(image: Annotated[Image, Depends(create_image_dep)]) -> ImageRead:
    return ImageRead.model_validate(image)


@router.delete("/{image_id}", status_code=200)
async def delete_image(_: Annotated[None, Depends(delete_image_dep)]) -> Result:
    return Result(status="ok")
