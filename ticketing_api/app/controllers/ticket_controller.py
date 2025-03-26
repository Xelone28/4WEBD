from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.ticket_schemas import TicketCreate, TicketRead
from app.services.ticket_service import TicketService
from app.database.database import get_db
from app.security import get_current_user
from app.schemas.user_schemas import UserRead

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)

@router.post("/", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket_data: TicketCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Créer un nouveau ticket.
    
    Seul un utilisateur authentifié peut créer un ticket.
    """
    ticket = await TicketService.create_ticket(db, ticket_data, current_user.id)

    if ticket is None:
        raise HTTPException(status_code=404, detail="Event not found.")
    if ticket == "No tickets available":
        raise HTTPException(status_code=400, detail="No tickets available for this event.")
    
    return ticket

@router.get("/{ticket_id}", response_model=TicketRead)
async def get_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Récupérer un ticket par son ID.
    
    Seul un utilisateur authentifié peut accéder à cette route.
    """
    ticket = await TicketService.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    
    # Optionnel : Vérifier que le ticket appartient à l'utilisateur ou que l'utilisateur est admin
    if ticket.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access forbidden.")
    
    return ticket

@router.get("/user/{user_id}", response_model=List[TicketRead])
async def get_tickets_by_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Récupérer tous les tickets pour un utilisateur spécifique.
    
    Seul l'utilisateur lui-même ou un administrateur peut accéder à cette route.
    """
    # Vérifier que l'utilisateur accédant à ses propres tickets ou est admin
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access forbidden.")
    
    tickets = await TicketService.get_tickets_by_user(db, user_id)
    return tickets    

@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserRead = Depends(get_current_user)
):
    """
    Annuler un ticket existant.
    
    Seul le propriétaire du ticket ou un administrateur peut annuler un ticket.
    """
    # Récupérer le ticket pour vérifier la propriété
    ticket = await TicketService.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    
    if ticket.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access forbidden.")
    
    success = await TicketService.delete_ticket(db, ticket_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return