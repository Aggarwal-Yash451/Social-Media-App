from .models import GroupCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.schema import Groups
from sqlmodel import select
from fastapi import HTTPException

class GroupService:
    async def create_group(self, group: GroupCreateModel, session: AsyncSession):
        group_model_dict = group.model_dump()
        new_group = Groups(**group_model_dict)
        session.add(new_group)
        await session.commit()
        await session.refresh(new_group)
        return new_group
    
    async def get_group(self, id: int, session: AsyncSession):
        statement = select(Groups).where(Groups.id == id)
        response = await session.exec(statement)
        group = response.first()
        if group is None:
            raise HTTPException(status_code=404, detail="Group not found")
        
        return group
    
    async def update_group(self, id: int,  new_group: GroupCreateModel, session: AsyncSession):
        group = await self.get_group(id, session)
        group.name = new_group.name
        group.description = new_group.description
        session.add(group)
        await session.commit()
        await session.refresh(group)
        return group
    
    async def delete_group(self, id: int, session: AsyncSession):
        group = await self.get_group(id, session)
        await session.delete(group)
        await session.commit()
        return "Group deleted success!"