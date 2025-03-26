# services/ticket_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.entities.ticket import Ticket
from app.schemas.ticket_schemas import TicketCreate, TicketRead
from typing import Optional, List
from fastapi import HTTPException, status

class TicketService:
    @staticmethod
    async def create_ticket(db: AsyncSession, ticket_create: TicketCreate, user_id: int) -> Optional[TicketRead]:
        # Vérifier que l'événement existe et qu'il y a des tickets disponibles
        event_stmt = select(Event).where(Event.id == ticket_create.event_id)
        event_result = await db.execute(event_stmt)
        event = event_result.scalars().first()
        
        if not event:
            return None
        if event.available_tickets <= 0:
            return "No tickets available"
        
        # Créer le ticket
        new_ticket = Ticket(
            ticket_number=ticket_create.ticket_number,
            event_id=ticket_create.event_id,
            user_id=user_id,
            purchase_date=ticket_create.purchase_date
        )
        db.add(new_ticket)
        
        # Mettre à jour les tickets disponibles
        event.available_tickets -= 1
        
        await db.commit()
        await db.refresh(new_ticket)
        return TicketRead.from_orm(new_ticket)
    
    @staticmethod
    async def get_ticket(db: AsyncSession, ticket_id: int) -> Optional[TicketRead]:
        stmt = select(Ticket).where(Ticket.id == ticket_id)
        result = await db.execute(stmt)
        ticket = result.scalars().first()
        return TicketRead.from_orm(ticket) if ticket else None
    
    @staticmethod
    async def get_tickets_by_user(db: AsyncSession, user_id: int) -> List[TicketRead]:
        stmt = select(Ticket).where(Ticket.user_id == user_id)
        result = await db.execute(stmt)
        tickets = result.scalars().all()
        return [TicketRead.from_orm(ticket) for ticket in tickets]
    
    @staticmethod
    async def delete_ticket(db: AsyncSession, ticket_id: int) -> bool:
        stmt = select(Ticket).where(Ticket.id == ticket_id)
        result = await db.execute(stmt)
        ticket = result.scalars().first()
        if not ticket:
            return False
        
        # Revenir les tickets disponibles
        event_stmt = select(Event).where(Event.id == ticket.event_id)
        event_result = await db.execute(event_stmt)
        event = event_result.scalars().first()
        if event:
            event.available_tickets += 1
        
        await db.delete(ticket)
        await db.commit()
        return True