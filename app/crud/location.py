import math
from typing import List

from sqlalchemy.orm import Session

from app.models.location import Location


def get_all(db: Session) -> List[Location]:
    return db.query(Location).all()


def _haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Great-circle distance in kilometres between two WGS-84 coordinates."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlng / 2) ** 2
    )
    return R * 2 * math.asin(math.sqrt(a))


def get_nearby(db: Session, lat: float, lng: float, radius_km: float) -> List[Location]:
    # Bounding-box pre-filter in the DB reduces the candidate set before the
    # exact Haversine calculation below.
    lat_delta = radius_km / 111.0
    lng_delta = radius_km / (111.0 * math.cos(math.radians(lat)))

    candidates = (
        db.query(Location)
        .filter(
            Location.lat.between(lat - lat_delta, lat + lat_delta),
            Location.lng.between(lng - lng_delta, lng + lng_delta),
        )
        .all()
    )

    return [
        loc
        for loc in candidates
        if _haversine_km(lat, lng, loc.lat, loc.lng) <= radius_km
    ]
