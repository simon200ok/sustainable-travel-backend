from typing import List

from sqlalchemy.orm import Session

from app.models.travel_log import TravelLog
from app.schemas.travel_log import TravelLogCreate


def get_by_user(db: Session, user_id: int) -> List[TravelLog]:
    return (
        db.query(TravelLog)
        .filter(TravelLog.user_id == user_id)
        .order_by(TravelLog.created_at.desc())
        .all()
    )


def create(db: Session, user_id: int, data: TravelLogCreate) -> TravelLog:
    entry = TravelLog(
        user_id=user_id,
        operator_id=data.operator_id,
        ticket_type=data.ticket_type,
        co2_saved_kg=data.co2_saved_kg,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
