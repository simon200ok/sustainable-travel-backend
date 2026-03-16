from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=False)
    ticket_type = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    # Duration category: Single | Day | Week | Month | Return
    duration = Column(String, nullable=False)
    notes = Column(String, nullable=True)

    operator = relationship("Operator", back_populates="tickets")
