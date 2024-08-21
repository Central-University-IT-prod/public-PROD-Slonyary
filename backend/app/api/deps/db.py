from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.session import get_db_session

SessionDepends = Annotated[AsyncSession, Depends(get_db_session)]
