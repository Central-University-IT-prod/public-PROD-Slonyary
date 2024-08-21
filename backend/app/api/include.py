from fastapi import APIRouter

from app.api.exceptions.handlers import exception_handlers
from app.api.routes import (
    auth,
    channels,
    draft,
    gpt_response,
    images,
    links,
    moderation,
    ping,
    posts,
)

api_router = APIRouter()

for router in (
    auth.router,
    posts.router,
    channels.router,
    ping.router,
    links.router,
    moderation.router,
    images.router,
    gpt_response.router,
    draft.router,
):
    api_router.include_router(router)


__all__ = ("api_router", "exception_handlers")
