from fastapi import APIRouter, Depends, status
from .models import GroupCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.database import get_session
from .service import GroupService

group_service = GroupService()
group_router = APIRouter()

@group_router.post("/create", response_model=GroupCreateModel, status_code=status.HTTP_200_OK)
async def create_group(group: GroupCreateModel, session: AsyncSession = Depends(get_session)):
    response = await group_service.create_group(group, session) 
    return response

@group_router.get("/get/{id}", response_model=GroupCreateModel, status_code=status.HTTP_201_CREATED)
async def get_group(id: int, session: AsyncSession = Depends(get_session)):
    response = await group_service.get_group(id, session)
    return response

@group_router.put("/update/{id}", response_model=GroupCreateModel, status_code=status.HTTP_202_ACCEPTED)
async def update_group(id: int, new_group: GroupCreateModel, session: AsyncSession = Depends(get_session)):
    response = await group_service.update_group(id, new_group, session)
    return response

@group_router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(id: int, session: AsyncSession = Depends(get_session)):
    response = await group_service.delete_group(id, session)
    return response