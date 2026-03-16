from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.ticket import TicketOut


class OperatorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    color: str
    description: Optional[str] = None
    website: Optional[str] = None
    sustainability_note: Optional[str] = None


class OperatorWithTickets(OperatorOut):
    """Operator detail view including all associated tickets."""

    tickets: List[TicketOut] = []
