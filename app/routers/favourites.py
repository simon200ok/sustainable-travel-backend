from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud import favourite as crud_favourite
from app.crud import operator as crud_operator
from app.database import get_db
from app.models.user import User
from app.schemas.favourite import FavouriteCreate, FavouriteOut
from app.schemas.response import APIResponse

router = APIRouter(prefix="/favourites", tags=["favourites"])


@router.get("", response_model=APIResponse[List[FavouriteOut]])
def get_favourites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> APIResponse[List[FavouriteOut]]:
    favourites = crud_favourite.get_by_user(db, user_id=current_user.id)
    return APIResponse(data=[FavouriteOut.model_validate(f) for f in favourites])


@router.post("", response_model=APIResponse[FavouriteOut], status_code=status.HTTP_201_CREATED)
def add_favourite(
    data: FavouriteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> APIResponse[FavouriteOut]:
    if not crud_operator.get_by_id(db, operator_id=data.operator_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operator not found.",
        )
    favourite = crud_favourite.create(db, user_id=current_user.id, operator_id=data.operator_id)
    if favourite is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This operator is already in your favourites.",
        )
    return APIResponse(data=FavouriteOut.model_validate(favourite), message="Added to favourites.")


@router.delete("/{favourite_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favourite(
    favourite_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    favourite = crud_favourite.get_by_id(db, favourite_id=favourite_id)
    if not favourite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favourite not found.",
        )
    if favourite.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to remove this favourite.",
        )
    crud_favourite.delete(db, favourite=favourite)
