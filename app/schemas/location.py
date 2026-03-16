from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class LocationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    lat: float
    lng: float
    description: Optional[str] = None
    nearby_transport: List[str] = []
    zone_id: Optional[int] = None
