from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.operator import OperatorOut


class TravelLogCreate(BaseModel):
    operator_id: int
    ticket_type: str = Field(min_length=1, max_length=100)
    co2_saved_kg: float = Field(default=0.0, ge=0)


class TravelLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    operator_id: int
    ticket_type: str
    co2_saved_kg: float
    created_at: datetime
    operator: OperatorOut
