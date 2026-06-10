import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from .config import Config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/1/auth/login")

SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM

async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Trying to decode token")
        return payload
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
