from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.api.deps.link_post_to_channel import dislink_post_dep, link_post_dep
from app.schemas import Result

router = APIRouter(prefix="/posts/{post_id}", tags=["links"])


@router.post("/link", status_code=status.HTTP_200_OK)
async def link_post(_: Annotated[None, Depends(link_post_dep)]) -> Result:
    return Result(status="ok")


@router.post("/dislink", status_code=status.HTTP_200_OK)
async def dislink_post(_: Annotated[None, Depends(dislink_post_dep)]) -> Result:
    return Result(status="ok")
