from typing import Optional

from pydantic import BaseModel, ConfigDict


class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    operator_id: int
    ticket_type: str
    price: float
    duration: str
    notes: Optional[str] = None
