from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class Posts(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(default=None, index=True, nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(default=None, foreign_key="users.id")


class UserGroupLink(SQLModel, table=True):
    user_id: int = Field(nullable=False, primary_key=True, foreign_key="users.id")
    group_id: int = Field(nullable=False, primary_key=True, foreign_key="groups.id")

class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    username: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    email: str = Field(nullable=False)
    groups: list["Groups"] = Relationship(back_populates="members", link_model=UserGroupLink)

class Groups(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: str 
    members: list["Users"] = Relationship(back_populates="groups", link_model=UserGroupLink)

