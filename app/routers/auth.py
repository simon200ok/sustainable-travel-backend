from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_current_user, verify_password
from app.crud import user as crud_user
from app.database import get_db
from app.schemas.response import APIResponse
from app.schemas.user import Token, UserCreate, UserLogin, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=APIResponse[Token],
    status_code=status.HTTP_201_CREATED,
)
def register(data: UserCreate, db: Session = Depends(get_db)) -> APIResponse[Token]:
    if crud_user.get_by_email(db, email=data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )
    crud_user.create(db, data=data)
    token = create_access_token(subject=data.email)
    return APIResponse(data=Token(access_token=token), message="Account created successfully.")


@router.post("/login", response_model=APIResponse[Token])
def login(data: UserLogin, db: Session = Depends(get_db)) -> APIResponse[Token]:
    user = crud_user.get_by_email(db, email=data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    token = create_access_token(subject=user.email)
    return APIResponse(data=Token(access_token=token), message="Login successful.")


@router.get("/me", response_model=APIResponse[UserOut])
def me(current_user=Depends(get_current_user)) -> APIResponse[UserOut]:
    return APIResponse(data=UserOut.model_validate(current_user))
