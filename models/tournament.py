from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime

from database import Base
from .associations import tournament_teams_association


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)

    results = relationship("TournamentResult", back_populates="tournament")

    teams = relationship(
        "Team", secondary=tournament_teams_association, back_populates="tournaments"
    )
