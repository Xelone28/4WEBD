from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.entities.event import Event
from app.schemas.event_schemas import EventCreate, EventUpdate

class EventService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_event(self, event: EventCreate) -> Event:
        db_event = Event(
            name=event.name,
            description=event.description,
            location=event.location,
            date=event.date,
            total_tickets=event.total_tickets,
            available_tickets=event.total_tickets
        )
        self.db.add(db_event)
        await self.db.commit()
        await self.db.refresh(db_event)
        return db_event

    async def get_event(self, event_id: int) -> Event:
        result = await self.db.execute(select(Event).where(Event.id == event_id))
        return result.scalars().first()

    async def get_all_events(self) -> list[Event]:
        result = await self.db.execute(select(Event))
        return result.scalars().all()

    async def update_event(self, event_id: int, event: EventUpdate) -> Event:
        db_event = await self.get_event(event_id)
        if not db_event:
            return None
        for var, value in vars(event).items():
            if value is not None:
                setattr(db_event, var, value)
        self.db.add(db_event)
        await self.db.commit()
        await self.db.refresh(db_event)
        return db_event

    async def delete_event(self, event_id: int) -> bool:
        db_event = await self.get_event(event_id)
        if not db_event:
            return False
        await self.db.delete(db_event)
        await self.db.commit()
        return True