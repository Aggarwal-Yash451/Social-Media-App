from pydantic import BaseModel

class PostCreateModel(BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponseModel(BaseModel):
    id: int
    title: str
    content: str
