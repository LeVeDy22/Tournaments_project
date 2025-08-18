from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    members = relationship("User", back_populates="team")
    results = relationship("TournamentResult", back_populates="team")
