from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.favourite import Favourite


def get_by_user(db: Session, user_id: int) -> List[Favourite]:
    return db.query(Favourite).filter(Favourite.user_id == user_id).all()


def get_by_id(db: Session, favourite_id: int) -> Optional[Favourite]:
    return db.query(Favourite).filter(Favourite.id == favourite_id).first()


def create(db: Session, user_id: int, operator_id: int) -> Optional[Favourite]:
    """Returns None if this operator is already favourited by the user."""
    favourite = Favourite(user_id=user_id, operator_id=operator_id)
    db.add(favourite)
    try:
        db.commit()
        db.refresh(favourite)
        return favourite
    except IntegrityError:
        db.rollback()
        return None


def delete(db: Session, favourite: Favourite) -> None:
    db.delete(favourite)
    db.commit()
