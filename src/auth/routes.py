from fastapi import APIRouter, Depends
from ..users.models import UserCreateModel, UserResponseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.database import get_session
from .services import  AuthService
from fastapi.security import OAuth2PasswordRequestForm

auth_service = AuthService()
auth_router = APIRouter()

@auth_router.post("/signup", response_model=UserResponseModel)
async def signup(user: UserCreateModel, session: AsyncSession = Depends(get_session)):
    new_user = await auth_service.signup(user, session)
    return new_user

@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    response = await auth_service.login(form_data.username, form_data.password, session)
    return response

