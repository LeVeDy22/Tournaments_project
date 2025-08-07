from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
import datetime


class Tournament(Base):
    __tablename__ = "tournaments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    description = Column(String(500))
    start_date = Column(default=datetime.datetime.utcnow)

    results = relationship("Result", back_populates="tournament")
