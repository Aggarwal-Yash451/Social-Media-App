from fastapi import APIRouter, Depends
from .service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.database import get_session
from ..auth_jwt import verify_token

user_router = APIRouter()
user_service = UserService()

@user_router.get("/get/me")
async def get_current_user(payload: dict = Depends(verify_token)):
    return {
        "user_id": payload["sub"]
    }

@user_router.get("/get/{id}")
async def get_user(id: int, session: AsyncSession = Depends(get_session)):
    response = await user_service.get_user(id, session)
    return response

