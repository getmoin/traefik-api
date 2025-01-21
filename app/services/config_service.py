import yaml
from fastapi import HTTPException
from app.core.config import settings

def load_config() -> dict:
    """Load the current Traefik configuration"""
    try:
        with open(settings.CONFIG_FILE, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load configuration: {str(e)}"
        )

def save_config(config: dict):
    """Save the Traefik configuration"""
    try:
        with open(settings.CONFIG_FILE, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save configuration: {str(e)}"
        )