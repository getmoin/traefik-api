from fastapi import APIRouter, HTTPException
from app.core.models import RouterServiceConfig
from app.services.config_service import load_config, save_config
from app.core.config import settings

router = APIRouter(prefix="/api")

@router.get("/router-service")
async def list_routers_services():
    """List all router and service configurations"""
    return load_config()

@router.post("/router-service")
async def add_router_and_service(config: RouterServiceConfig):
    """Add a new router and service configuration"""
    try:
        current_config = load_config()
        
        # Add router configuration
        current_config['http']['routers'][config.router_name] = {
            "rule": f"Host(`{config.config.domain}`)",
            "service": config.config.service_name,
            "entryPoints": config.config.entry_points,
            "tls": {
                "certResolver": settings.CERT_RESOLVER,
                "domains": [{
                    "main": config.config.domain,
                    "sans": [f"*.{config.config.domain}"]
                }]
            } if config.config.enable_tls else {}
        }

        # Add service configuration
        current_config['http']['services'][config.config.service_name] = {
            "loadBalancer": {
                "servers": [{"url": config.service_url}]
            }
        }
        
        save_config(current_config)
        return {"status": "success", "message": "Router and service added successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add router and service: {str(e)}"
        )