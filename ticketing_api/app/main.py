from fastapi import FastAPI
from app.controllers import user_controller, event_controller, ticket_controller
from app.database.database import engine
from app.database.base import Base  # ← base commune pour tous les modèles
from app.entities import *  # ← force l'import de tous les modèles pour éviter les erreurs de mapping
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Ticketing System API",
    description="API for handling concerts and events tickets.",
    version="1.0.0"
)
# Define allowed origins (CORS policy)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(user_controller.router)
app.include_router(event_controller.router)
app.include_router(ticket_controller.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Ticketing System API"}

# Initialisation de la base de données au démarrage
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)