from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.zone import Zone


def get_all(db: Session) -> List[Zone]:
    return db.query(Zone).all()


def get_by_id(db: Session, zone_id: int) -> Optional[Zone]:
    return db.query(Zone).filter(Zone.id == zone_id).first()
