from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.entities.ticket import Ticket
from app.entities.event import Event
from app.schemas.ticket_schemas import TicketCreate
import uuid

class TicketService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_ticket(self, ticket_data: TicketCreate) -> Ticket:
        """ Create a ticket if available tickets exist for the event """
        event = await self.db.execute(select(Event).where(Event.id == ticket_data.event_id))
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

        self.db.add(new_ticket)
        await self.db.commit()
        await self.db.refresh(new_ticket)
        return new_ticket

    async def get_ticket(self, ticket_id: int) -> dict:
    result = await self.db.execute(
        select(Ticket, Event.name, User.email)
        .join(Event, Ticket.event_id == Event.id)
        .join(User, Ticket.user_id == User.id)
        .where(Ticket.id == ticket_id)
    )
    ticket, user_email = result.first()

    return {
        "id": ticket.id,
        "ticket_number": ticket.ticket_number,
        "event_id": ticket.event_id,
        "user_id": ticket.user_id,
        "user_email": user_email,
        "purchase_date": ticket.purchase_date
    }

    async def get_tickets_by_user(self, user_id: int) -> list[Ticket]:
        """ Retrieve all tickets for a given user """
        result = await self.db.execute(select(Ticket).where(Ticket.user_id == user_id))
        return result.scalars().all()

    async def delete_ticket(self, ticket_id: int) -> bool:
        """ Cancel a ticket and restore the event's availability """
        ticket = await self.get_ticket(ticket_id)
        if not ticket:
            return False

        # Restore available tickets for the event
        event = await self.db.execute(select(Event).where(Event.id == ticket.event_id))
        event = event.scalars().first()
        if event:
            event.available_tickets += 1  # Restore the ticket availability

        await self.db.delete(ticket)
        await self.db.commit()
        return True