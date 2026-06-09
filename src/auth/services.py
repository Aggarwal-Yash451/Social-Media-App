from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.schema import Users
from sqlmodel import select
from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta
from ..config import Config
from ..users.models import UserCreateModel

password_hash = PasswordHash.recommended()
SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Config.ACCESS_TOKEN_EXPIRE_MINUTES

class AuthService:
    async def signup(self, user: UserCreateModel, session: AsyncSession):
        user_data_dict = user.model_dump()
        password = user_data_dict["password"]
        hashed_password = password_hash.hash(password)
        user_data_dict["password"] = hashed_password
        new_user = Users(**user_data_dict)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    async def login(self, username: str, password: str, session: AsyncSession):
        statement = select(Users).where(Users.username == username)
        check_db = await session.exec(statement)
        db_user = check_db.first()
        if(db_user is None):
            return {"message": "User with username not found. Signup to continue"}

        isPasswordCorrect = password_hash.verify(password, db_user.password)

        payload = {
            "sub": str(db_user.id),
            "exp": datetime.utcnow() +  timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        if(isPasswordCorrect):
            token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
            print(f"Token: {token}")
            return {
                "access_token": token,
                "token_type": "bearer"
            }
        
        else:
            return {"message": "Incorrect password"}