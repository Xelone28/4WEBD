# schemas/ticket_schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketBase(BaseModel):
    ticket_number: str
    event_id: int
    purchase_date: Optional[datetime] = None

class TicketCreate(TicketBase):
    pass

class TicketRead(TicketBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True