from fastapi import FastAPI
from app.controllers import user_controller, event_controller
from app.database.database import engine
from app.entities.user import Base as UserBase
from app.entities.event import Base as EventBase
from app.entities.ticket import Base as TicketBase
import uvicorn

app = FastAPI(
    title="Ticketing System API",
    description="API for handling concerts and events tickets.",
    version="1.0.0"
)

# Include routers
app.include_router(user_controller.router)
app.include_router(event_controller.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Ticketing System API"}

# Create database tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(UserBase.metadata.create_all)
        await conn.run_sync(EventBase.metadata.create_all)
        await conn.run_sync(TicketBase.metadata.create_all)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)