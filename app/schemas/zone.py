from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ZoneOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    color: str
    description: Optional[str] = None
    areas: List[str] = []
    metro_stations: List[str] = []
