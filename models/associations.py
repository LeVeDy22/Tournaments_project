from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

tournament_teams_association = Table(
    "tournament_teams",
    Base.metadata,
    Column("tournament_id", Integer, ForeignKey("tournaments.id"), primary_key=True),
    Column("team_id", Integer, ForeignKey("teams.id"), primary_key=True),
)
