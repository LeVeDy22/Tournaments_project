from pydantic import BaseModel
from typing import Optional, List
import datetime
from .user import User


class TeamBase(BaseModel):
    name: str


class TeamCreate(TeamBase):
    pass


class TeamInTournament(TeamBase):
    id: int

    class Config:
        from_attributes = True


class TournamentBase(BaseModel):
    name: str
    description: Optional[str] = None


class TournamentCreate(TournamentBase):
    pass


class TournamentInTeam(TournamentBase):
    id: int

    class Config:
        from_attributes = True


class Team(TeamBase):
    id: int
    members: List[User] = []
    tournaments: List[TournamentInTeam] = []

    class Config:
        from_attributes = True


class Tournament(TournamentBase):
    id: int
    start_date: datetime.datetime
    teams: List[TeamInTournament] = []

    class Config:
        from_attributes = True
