from fastapi import APIRouter, Depends
from .models import PostCreateModel, PostResponseModel
from .service import PostServie
from ..db.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

post_router = APIRouter()
post_service = PostServie()

@post_router.get("/get-all", response_model=list[PostResponseModel])
async def get_all_posts(session: AsyncSession = Depends(get_session)):
    posts = await post_service.get_all_posts(session)
    return posts

@post_router.post("/create")
async def create_post(post: PostCreateModel, session: AsyncSession = Depends(get_session)):
    new_post = await post_service.create_post(post, session)
    return new_post

@post_router.get("/get/{id}", response_model=PostResponseModel)
async def get_post(id: int, session: AsyncSession = Depends(get_session)):
    post = await post_service.get_post(id, session)
    return post

@post_router.put("/update/{id}")
async def update_post(id: int, post_content: PostCreateModel, session: AsyncSession = Depends(get_session)):
    post = await post_service.update_post(id, post_content, session)
    return post


@post_router.delete("/delete/{id}")
async def delete_post(id: int, session: AsyncSession = Depends(get_session)):
    await post_service.delete_post(id, session)
    return "Post deletion success"
