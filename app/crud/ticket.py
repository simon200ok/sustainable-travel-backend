from typing import List

from sqlalchemy.orm import Session

from app.models.ticket import Ticket


def get_all(db: Session) -> List[Ticket]:
    return db.query(Ticket).all()


def get_by_operator(db: Session, operator_id: int) -> List[Ticket]:
    return db.query(Ticket).filter(Ticket.operator_id == operator_id).all()
