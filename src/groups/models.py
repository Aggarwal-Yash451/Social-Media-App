from pydantic import BaseModel

class GroupCreateModel(BaseModel):
    name: str
    description: str | None
    