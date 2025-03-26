from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.entities.event import Event
from app.schemas.event_schemas import EventCreate, EventUpdate

class EventService:
    @staticmethod
    async def create_event(db: AsyncSession, event: EventCreate) -> Event:
        db_event = Event(
            name=event.name,
            description=event.description,
            location=event.location,
            date=event.date,
            total_tickets=event.total_tickets,
            available_tickets=event.total_tickets
        )
        db.add(db_event)
        await db.commit()
        await db.refresh(db_event)
        return db_event
    
    @staticmethod
    async def get_event(db: AsyncSession, event_id: int) -> Event:
        result = await db.execute(select(Event).where(Event.id == event_id))
        return result.scalars().first()
    
    @staticmethod
    async def get_all_events(db: AsyncSession) -> list[Event]:
        result = await db.execute(select(Event))
        return result.scalars().all()
    
    @staticmethod
    async def update_event(db: AsyncSession, event_id: int, event: EventUpdate) -> Event:
        db_event = await EventService.get_event(event_id)
        if not db_event:
            return None
        for var, value in vars(event).items():
            if value is not None:
                setattr(db_event, var, value)
        db.add(db_event)
        await db.commit()
        await db.refresh(db_event)
        return db_event
    
    @staticmethod
    async def delete_event(db: AsyncSession, event_id: int) -> bool:
        db_event = await EventService.get_event(event_id)
        if not db_event:
            return False
        await db.delete(db_event)
        await db.commit()
        return True