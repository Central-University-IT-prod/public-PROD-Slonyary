from app.schemas.base import BaseSchema


class ImageIn(BaseSchema):
    base64: str


class ImageCreate(BaseSchema):
    post_id: int
    base64: str


class ImageRead(BaseSchema):
    id: int
    post_id: int
    base64: str


class ImageUpdate(BaseSchema):
    pass
