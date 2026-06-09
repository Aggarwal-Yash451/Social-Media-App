from pydantic import BaseModel

class UserCreateModel(BaseModel):
    username: str
    password: str
    name: str
    email: str

class UserResponseModel(BaseModel):
    name: str
    username: str
    email: str