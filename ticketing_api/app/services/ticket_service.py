from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.entities.ticket import Ticket
from app.entities.event import Event
from app.entities.user import User  # ✅ Manquait ici
from app.schemas.ticket_schemas import TicketCreate
import uuid

class TicketService:

    @staticmethod
    async def create_ticket(db: AsyncSession, ticket_data: TicketCreate) -> Ticket:
        """ Create a ticket if available tickets exist for the event """
        event = await db.execute(select(Event).where(Event.id == ticket_data.event_id))
        event = event.scalars().first()

        if not event:
            return None  # Event does not exist
        
        if event.available_tickets <= 0:
            return "No tickets available"

        # Generate a unique ticket number
        ticket_number = str(uuid.uuid4())

        new_ticket = Ticket(
            ticket_number=ticket_number,
            event_id=ticket_data.event_id,
            user_id=ticket_data.user_id
        )
        
        # Update available tickets
        event.available_tickets -= 1

        db.add(new_ticket)
        await db.commit()
        await db.refresh(new_ticket)
        return new_ticket
    
    @staticmethod
    async def get_ticket(db: AsyncSession, ticket_id: int) -> dict:
        result = await db.execute(
            select(Ticket, Event.name, User.email)
            .join(Event, Ticket.event_id == Event.id)
            .join(User, Ticket.user_id == User.id)
            .where(Ticket.id == ticket_id)
        )
        ticket, event = result.first()

        return {
            "id": ticket.id,
            "ticket_number": ticket.ticket_number,
            "event_id": ticket.event_id,
            "user_id": ticket.user_id,
            "purchase_date": ticket.purchase_date
        }
    
    @staticmethod
    async def get_tickets_by_user(db: AsyncSession, user_id: int) -> list[Ticket]:
        """ Retrieve all tickets for a given user """
        result = await db.execute(select(Ticket).where(Ticket.user_id == user_id))
        return result.scalars().all()
    
    @staticmethod
    async def delete_ticket(db: AsyncSession, ticket_id: int) -> bool:
        """ Cancel a ticket and restore the event's availability """
        ticket = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
        ticket = ticket.scalars().first()

        if not ticket:
            return False

        event = await db.execute(select(Event).where(Event.id == ticket.event_id))
        event = event.scalars().first()
        if event:
            event.available_tickets += 1

        await db.delete(ticket)
        await db.commit()
        return True