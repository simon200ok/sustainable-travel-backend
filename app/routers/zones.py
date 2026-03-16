from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import zone as crud_zone
from app.database import get_db
from app.schemas.response import APIResponse
from app.schemas.zone import ZoneOut

router = APIRouter(prefix="/zones", tags=["zones"])


@router.get("", response_model=APIResponse[List[ZoneOut]])
def get_zones(db: Session = Depends(get_db)) -> APIResponse[List[ZoneOut]]:
    zones = crud_zone.get_all(db)
    return APIResponse(data=[ZoneOut.model_validate(z) for z in zones])


@router.get("/{zone_id}", response_model=APIResponse[ZoneOut])
def get_zone(
    zone_id: int,
    db: Session = Depends(get_db),
) -> APIResponse[ZoneOut]:
    zone = crud_zone.get_by_id(db, zone_id=zone_id)
    if not zone:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zone not found.",
        )
    return APIResponse(data=ZoneOut.model_validate(zone))
