from pydantic import BaseModel


class ResultBase(BaseModel):
    score: int


class ResultCreate(ResultBase):
    team_id: int
    tournament_id: int


class Result(ResultBase):
    id: int
    team_id: int
    tournament_id: int

    class Config:
        orm_mode = True
