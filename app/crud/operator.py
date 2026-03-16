from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.operator import Operator


def get_all(db: Session) -> List[Operator]:
    return db.query(Operator).all()


def get_by_id(db: Session, operator_id: int) -> Optional[Operator]:
    return db.query(Operator).filter(Operator.id == operator_id).first()


def get_by_type(db: Session, transport_type: str) -> List[Operator]:
    return db.query(Operator).filter(Operator.type == transport_type).all()
