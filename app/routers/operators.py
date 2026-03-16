from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud import operator as crud_operator
from app.database import get_db
from app.schemas.operator import OperatorOut, OperatorWithTickets
from app.schemas.response import APIResponse

router = APIRouter(prefix="/operators", tags=["operators"])


@router.get("", response_model=APIResponse[List[OperatorOut]])
def get_operators(
    type: Optional[str] = Query(None, description="Filter by transport type: Bus, Metro, Train"),
    db: Session = Depends(get_db),
) -> APIResponse[List[OperatorOut]]:
    if type:
        operators = crud_operator.get_by_type(db, transport_type=type)
    else:
        operators = crud_operator.get_all(db)
    return APIResponse(data=[OperatorOut.model_validate(op) for op in operators])


@router.get("/{operator_id}", response_model=APIResponse[OperatorWithTickets])
def get_operator(
    operator_id: int,
    db: Session = Depends(get_db),
) -> APIResponse[OperatorWithTickets]:
    operator = crud_operator.get_by_id(db, operator_id=operator_id)
    if not operator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operator not found.",
        )
    return APIResponse(data=OperatorWithTickets.model_validate(operator))
