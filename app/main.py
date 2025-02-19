from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import router_service, backup
from app.core.config import settings
import uvicorn
import asyncio
from app.services.backup_scheduler import schedule_backups

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Schedule backup task
    backup_task = asyncio.create_task(schedule_backups())
    yield
    # Shutdown: Cancel backup task
    backup_task.cancel()
    try:
        await backup_task
    except asyncio.CancelledError:
        pass

app = FastAPI(title="Traefik Configuration Manager", lifespan=lifespan)

app.include_router(router_service.router)
app.include_router(backup.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT) 