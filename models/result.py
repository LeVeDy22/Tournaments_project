from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)

    team_id = Column(Integer, ForeignKey("teams.id"))
    team = relationship("Team", back_populates="results")

    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    tournament = relationship("Tournament", back_populates="results")
