from app.schemas.base import BaseSchema


class JwtToken(BaseSchema):
    token: str
