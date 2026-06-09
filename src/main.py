from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from src.db.database import init_db
from .posts.routes import post_router
from .auth.routes import auth_router
from .users.routes import user_router
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_dep = Annotated[str, Depends(oauth2_scheme)]

@asynccontextmanager
async def life_span(app: FastAPI):
    from .db.schema import Posts, Users
    print("Server is starting...")
    await init_db()
    yield
    print("Server is stopping...")

version = "1"

app = FastAPI(
    lifespan=life_span,
    title="Social media",
    version=version
)

@app.get("/")
async def root():
    return {"message": "The is the home screen"}


app.include_router(post_router, prefix=f"/api/{version}/posts", tags=["Posts"])
app.include_router(user_router, prefix=f"/api/{version}/users", tags=["Users"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])