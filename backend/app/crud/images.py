from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CrudBase
from app.schemas import ImageCreate, ImageRead, ImageUpdate
from shared.database.models import Image


class CrudImage(CrudBase[Image, ImageCreate, ImageRead, ImageUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Image)
