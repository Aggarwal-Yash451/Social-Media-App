from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.schema import Posts
from .models import PostCreateModel

class PostService:
    async def get_all_posts(self, user_id, session:AsyncSession):
        statement = select(Posts).where(Posts.user_id == user_id).order_by(Posts.id)
        result = await session.exec(statement=statement)
        return result.all()
    
    async def create_post(self, post: PostCreateModel,  user_id: int, session: AsyncSession):
        post_data_dict = post.model_dump()
        post_data_dict["user_id"] = user_id
        new_post = Posts(**post_data_dict)
        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)
        return new_post

    async def get_post(self, id: int, user_id: int, session: AsyncSession):
        statement = select(Posts).where(Posts.id == id)
        post = await session.exec(statement)
        
        if(post == None):
            return None
        
        db_post = post.first()

        if db_post.user_id != user_id:
            return None

        return db_post
    
    async def update_post(self, id: int, user_id: int, post_content: PostCreateModel, session: AsyncSession):
        post = await self.get_post(id, user_id, session)
        if(post == None):
            return None
        post.title = post_content.title
        post.content = post_content.content
        post.published = post_content.published

        session.add(post)
        await session.commit()
        await session.refresh(post)

        return post
    
    async def delete_post(self, id: int, user_id: int, session: AsyncSession):
        post = await self.get_post(id, user_id, session)
        if(post == None): 
            return
        await session.delete(post)
        await session.commit()