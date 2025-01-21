from pydantic import BaseModel, Field
from typing import List

class ServiceConfig(BaseModel):
    url: str = Field(..., example="http://localhost:8080")

class RouterConfig(BaseModel):
    domain: str = Field(..., example="api.example.com")
    service_name: str = Field(..., example="my-service")
    entry_points: List[str] = Field(default=["websecure"])
    enable_tls: bool = Field(default=False)
    middlewares: List[str] = Field(default_factory=list)

class RouterServiceConfig(BaseModel):
    router_name: str
    config: RouterConfig
    service_url: str

class ConfigBackup(BaseModel):
    backup_key: str
    timestamp: str
    location: str  # 's3' or 'local' 