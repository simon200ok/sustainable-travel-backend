from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    # Transport mode: Bus | Metro | Train
    type = Column(String, nullable=False)
    color = Column(String, nullable=False)
    description = Column(String, nullable=True)
    website = Column(String, nullable=True)
    sustainability_note = Column(String, nullable=True)

    tickets = relationship("Ticket", back_populates="operator", cascade="all, delete-orphan")
    favourites = relationship("Favourite", back_populates="operator")
    travel_logs = relationship("TravelLog", back_populates="operator")
