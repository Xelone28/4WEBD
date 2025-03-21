from pydantic import BaseModel
from datetime import datetime

class TicketRead(BaseModel):
    id: int
    ticket_number: str
    event_id: int
    user_id: int
    purchase_date: datetime

    class Config:
        orm_mode = True
