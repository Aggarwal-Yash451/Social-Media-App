from sqlmodel import SQLModel, Field
from datetime import datetime

class Posts(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(default=None, index=True, nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    username: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    email: str = Field(nullable=False)
