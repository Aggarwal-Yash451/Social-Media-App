from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from ..db.schema import Users

class UserService:
    async def get_user(self, id: int, session: AsyncSession):
        statement = select(Users).where(Users.id == id)
        response = await session.exec(statement)
        return response.first()