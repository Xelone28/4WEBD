from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.event_schemas import EventCreate, EventRead, EventUpdate
from app.services.event_service import EventService
from app.database.database import get_db

router = APIRouter(
    prefix="/events",
    tags=["events"]
)

@router.post("/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreate, db: AsyncSession = Depends(get_db)):
    event_service = EventService(db)
    created_event = await event_service.create_event(event)
    return created_event

@router.get("/{event_id}", response_model=EventRead)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    event_service = EventService(db)
    event = await event_service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")
    return event

@router.get("/", response_model=List[EventRead])
async def get_all_events(db: AsyncSession = Depends(get_db)):
    event_service = EventService(db)
    events = await event_service.get_all_events()
    return events

@router.put("/{event_id}", response_model=EventRead)
async def update_event(event_id: int, event: EventUpdate, db: AsyncSession = Depends(get_db)):
    event_service = EventService(db)
    updated_event = await event_service.update_event(event_id, event)
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found.")
    return updated_event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int, db: AsyncSession = Depends(get_db)):
    event_service = EventService(db)
    success = await event_service.delete_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found.")
    return