from pydantic import BaseModel
from typing import List
from .user import User


class TeamBase(BaseModel):
    name: str


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int
    members: List[User] = []

    class Config:
        from_attributes = True
