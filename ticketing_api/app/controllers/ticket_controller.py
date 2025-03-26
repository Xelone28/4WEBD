from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.ticket_schemas import TicketCreate, TicketRead
from app.services.ticket_service import TicketService
from app.database.database import get_db

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)

@router.post("/", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket_data: TicketCreate, db: AsyncSession = Depends(get_db)):
    """ Create a new ticket """
    ticket = await TicketService.create_ticket(db, ticket_data)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Event not found.")
    if ticket == "No tickets available":
        raise HTTPException(status_code=400, detail="No tickets available for this event.")
    
    return ticket

@router.get("/{ticket_id}", response_model=TicketRead)
async def get_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    return await TicketService.get_ticket(db, ticket_id)

@router.get("/user/{user_id}", response_model=List[TicketRead])
async def get_tickets_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """ Retrieve all tickets for a user """
    return await TicketService.get_tickets_by_user(db, user_id)    

@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    """ Cancel a ticket """
    success = await TicketService.delete_ticket(db, ticket_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    
    return