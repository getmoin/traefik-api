import yaml
from fastapi import HTTPException
from app.core.config import settings

def load_config():
    """Load configuration from file"""
    try:
        with open(settings.CONFIG_FILE, 'r') as f:
            config = yaml.safe_load(f)
            
        # Initialize empty structure if config is None
        if config is None:
            config = {
                'http': {
                    'routers': {},
                    'services': {}
                }
            }
            # Save the initial structure
            save_config(config)
            
        return config
    except FileNotFoundError:
        # Create initial configuration structure
        config = {
            'http': {
                'routers': {},
                'services': {}
            }
        }
        # Save the initial structure
        save_config(config)
        return config

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