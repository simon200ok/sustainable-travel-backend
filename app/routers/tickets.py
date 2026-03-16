from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import operator as crud_operator
from app.crud import ticket as crud_ticket
from app.database import get_db
from app.schemas.response import APIResponse
from app.schemas.ticket import TicketOut

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("", response_model=APIResponse[List[TicketOut]])
def get_all_tickets(db: Session = Depends(get_db)) -> APIResponse[List[TicketOut]]:
    tickets = crud_ticket.get_all(db)
    return APIResponse(data=[TicketOut.model_validate(t) for t in tickets])


@router.get("/operator/{operator_id}", response_model=APIResponse[List[TicketOut]])
def get_tickets_by_operator(
    operator_id: int,
    db: Session = Depends(get_db),
) -> APIResponse[List[TicketOut]]:
    if not crud_operator.get_by_id(db, operator_id=operator_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operator not found.",
        )
    tickets = crud_ticket.get_by_operator(db, operator_id=operator_id)
    return APIResponse(data=[TicketOut.model_validate(t) for t in tickets])
