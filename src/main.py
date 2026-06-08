from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.database import init_db
from .posts.routes import post_router

@asynccontextmanager
async def life_span(app: FastAPI):
    from .db.schema import Posts
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
    return {"message": "This is the home screen"}


app.include_router(post_router, prefix=f"/api/{version}/posts")