from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Favourite(Base):
    __tablename__ = "favourites"
    # Prevent duplicate user/operator pairs at the DB level
    __table_args__ = (UniqueConstraint("user_id", "operator_id", name="uq_user_operator"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="favourites")
    operator = relationship("Operator", back_populates="favourites")
