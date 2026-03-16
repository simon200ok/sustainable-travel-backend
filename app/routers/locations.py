from typing import Annotated, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.crud import location as crud_location
from app.database import get_db
from app.schemas.location import LocationOut
from app.schemas.response import APIResponse

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("", response_model=APIResponse[List[LocationOut]])
def get_all_locations(db: Session = Depends(get_db)) -> APIResponse[List[LocationOut]]:
    locations = crud_location.get_all(db)
    return APIResponse(data=[LocationOut.model_validate(loc) for loc in locations])


@router.get("/nearby", response_model=APIResponse[List[LocationOut]])
def get_nearby_locations(
    lat: Annotated[float, Query(ge=-90, le=90, description="Latitude of the search centre")],
    lng: Annotated[float, Query(ge=-180, le=180, description="Longitude of the search centre")],
    radius: Annotated[int, Query(ge=1, le=50, description="Search radius in kilometres")] = 5,
    db: Session = Depends(get_db),
) -> APIResponse[List[LocationOut]]:
    nearby = crud_location.get_nearby(db, lat=lat, lng=lng, radius_km=float(radius))
    return APIResponse(
        data=[LocationOut.model_validate(loc) for loc in nearby],
        message=f"Found {len(nearby)} location(s) within {radius} km.",
    )
