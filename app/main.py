from fastapi import FastAPI
from app.api import router_service, backup
from app.core.config import settings
import uvicorn

app = FastAPI(title="Traefik Configuration Manager")

app.include_router(router_service.router)
app.include_router(backup.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT) 