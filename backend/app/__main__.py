import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.include import api_router, exception_handlers
from shared.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0] if route.tags else 'Route'}-{route.name}"


app = FastAPI(
    generate_unique_id_function=custom_generate_unique_id,
    root_path=settings.API_STR,
    exception_handlers=exception_handlers,
)

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


def main() -> None:
    uvicorn.run(app=app, host="0.0.0.0", port=8090)


if __name__ == "__main__":
    main()
