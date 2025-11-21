from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    team_name: str

class UserOut(BaseModel):
    id: int
    name: str
    is_active: bool
    team_id: Optional[int]

    class Config:
        from_attributes = True