from fastapi import APIRouter, Depends, status
from .models import PostCreateModel, PostResponseModel
from .service import PostService
from ..db.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from ..auth_jwt import verify_token


post_router = APIRouter()
post_service = PostService()

@post_router.get("/get-all", response_model=list[PostResponseModel], status_code=status.HTTP_200_OK)
async def get_all_posts(payload: dict = Depends(verify_token), session: AsyncSession = Depends(get_session)):
    user_id = int(payload["sub"])
    posts = await post_service.get_all_posts(user_id, session)
    return posts

@post_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreateModel, session: AsyncSession = Depends(get_session), payload: dict = Depends(verify_token)):
    user_id = int(payload["sub"])
    new_post = await post_service.create_post(post, user_id, session)
    return new_post

@post_router.get("/get/{id}", response_model=PostResponseModel, status_code=status.HTTP_200_OK)
async def get_post(id: int, payload: dict = Depends(verify_token), session: AsyncSession = Depends(get_session)):
    user_id = int(payload["sub"])
    post = await post_service.get_post(id, user_id, session)
    return post

@post_router.put("/update/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, post_content: PostCreateModel, payload: dict = Depends(verify_token), session: AsyncSession = Depends(get_session)):
    user_id = int(payload["sub"])
    post = await post_service.update_post(id, user_id, post_content, session)
    return post

@post_router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, payload: dict = Depends(verify_token), session: AsyncSession = Depends(get_session)):
    user_id = int(payload["sub"])
    await post_service.delete_post(id, user_id, session)
    return "Post deletion success"
    