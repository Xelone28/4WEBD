from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TicketCreate(BaseModel):
    """ Schema for creating a ticket """
    event_id: int
    user_id: int


class TicketRead(BaseModel):
    """ Schema for reading ticket details """
    id: int
    ticket_number: str
    event_id: int
    user_id: int
    purchase_date: datetime

    class Config:
        from_attributes = True  