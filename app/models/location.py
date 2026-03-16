from sqlalchemy import Column, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from app.database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    # Type determines map marker colour: campus | metro | train | bus
    type = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    nearby_transport = Column(JSON, default=list)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=True)

    zone = relationship("Zone", back_populates="locations")
