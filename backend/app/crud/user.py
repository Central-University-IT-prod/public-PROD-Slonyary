from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CrudBase
from app.schemas import UserCreate, UserRead, UserUpdate
from shared.database.models.users import User


class CrudUser(CrudBase[User, UserCreate, UserRead, UserUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def is_exists(self, id: int) -> bool:
        return bool(await self.get(id))
