from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud import operator as crud_operator
from app.crud import travel_log as crud_travel_log
from app.database import get_db
from app.models.user import User
from app.schemas.response import APIResponse
from app.schemas.travel_log import TravelLogCreate, TravelLogOut

router = APIRouter(prefix="/travel-log", tags=["travel-log"])


@router.get("", response_model=APIResponse[List[TravelLogOut]])
def get_travel_log(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> APIResponse[List[TravelLogOut]]:
    logs = crud_travel_log.get_by_user(db, user_id=current_user.id)
    return APIResponse(data=[TravelLogOut.model_validate(entry) for entry in logs])


@router.post("", response_model=APIResponse[TravelLogOut], status_code=status.HTTP_201_CREATED)
def log_journey(
    data: TravelLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> APIResponse[TravelLogOut]:
    if not crud_operator.get_by_id(db, operator_id=data.operator_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operator not found.",
        )
    entry = crud_travel_log.create(db, user_id=current_user.id, data=data)
    return APIResponse(data=TravelLogOut.model_validate(entry), message="Journey logged successfully.")
