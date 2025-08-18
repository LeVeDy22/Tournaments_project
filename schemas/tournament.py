from pydantic import BaseModel
from typing import Optional
import datetime


class TournamentBase(BaseModel):
    name: str
    description: Optional[str] = None


class TournamentCreate(TournamentBase):
    pass


class Tournament(TournamentBase):
    id: int
    start_date: datetime.datetime

    class Config:
        from_attributes = True
