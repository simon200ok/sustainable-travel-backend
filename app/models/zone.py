from sqlalchemy import Column, Integer, JSON, String
from sqlalchemy.orm import relationship

from app.database import Base


class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    color = Column(String, nullable=False)
    description = Column(String, nullable=True)
    # JSON lists stored natively in PostgreSQL, as text in SQLite
    areas = Column(JSON, default=list)
    metro_stations = Column(JSON, default=list)

    locations = relationship("Location", back_populates="zone")
