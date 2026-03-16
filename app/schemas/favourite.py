from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.operator import OperatorOut


class FavouriteCreate(BaseModel):
    operator_id: int


class FavouriteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    operator_id: int
    created_at: datetime
    operator: OperatorOut
