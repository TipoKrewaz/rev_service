from pydantic import BaseModel
from typing import List

class PRCreate(BaseModel):
    title: str
    author_id: int

class PRReassign(BaseModel):
    old_reviewer_id: int

class PROut(BaseModel):
    id: int
    title: str
    author_id: int
    status: str
    reviewers: List[int]

    class Config:
        from_attributes = True