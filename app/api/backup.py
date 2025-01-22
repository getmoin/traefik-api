from fastapi import APIRouter, HTTPException, Depends, Header
from datetime import datetime
import os
import yaml
from app.core.config import settings
from app.services.config_service import load_config
from app.services.backup_service import create_backup

router = APIRouter(prefix="/api")

# Load the API key from the environment
API_KEY = os.getenv("API_KEY")

def api_key_auth(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

@router.post("/backup", dependencies=[Depends(api_key_auth)])
async def create_config_backup():
    """Create a backup of the current configuration"""
    try:
        # Create timestamp for backup
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        # Create backup using backup service
        backup_result = create_backup(timestamp)
        
        # Ensure local backup exists regardless of S3 status
        backup_filename = f"traefik_config_{timestamp}.yaml"
        local_backup_path = os.path.join(settings.LOCAL_BACKUP_DIR, backup_filename)
        
        # Ensure backup directory exists
        os.makedirs(settings.LOCAL_BACKUP_DIR, exist_ok=True)
        
        # Create local backup
        current_config = load_config()
        with open(local_backup_path, 'w') as f:
            yaml.dump(current_config, f, default_flow_style=False)
        
        response = {
            "status": "success",
            "backup": {
                "filename": backup_filename,
                "local_path": local_backup_path,
                "timestamp": timestamp,
            }
        }
        
        # Add S3 information if backup was created in S3
        if backup_result.location == 's3':
            response["backup"]["s3_key"] = backup_result.backup_key
            print(f"Backup successfully created in S3: {backup_result.backup_key}")
        else:
            print("Backup created locally only. S3 backup was not created.")
            if settings.ENABLE_S3_BACKUP:
                print("S3 backup was enabled but failed. Check S3 configuration and permissions.")
        
        return response
        
    except Exception as e:
        error_msg = f"Failed to create backup: {str(e)}"
        print(error_msg)  # Log the error
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )

@router.get("/backup", dependencies=[Depends(api_key_auth)])
async def list_backups():
    """List all available backups"""
    try:
        backups = []
        if os.path.exists(settings.LOCAL_BACKUP_DIR):
            for filename in os.listdir(settings.LOCAL_BACKUP_DIR):
                if filename.endswith('.yaml'):
                    file_path = os.path.join(settings.LOCAL_BACKUP_DIR, filename)
                    stat = os.stat(file_path)
                    backups.append({
                        "filename": filename,
                        "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "size": stat.st_size
                    })
        
        return {
            "status": "success",
            "backups": sorted(backups, key=lambda x: x['created_at'], reverse=True)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list backups: {str(e)}"
        )

@router.get("/backup/{backup_key}", dependencies=[Depends(api_key_auth)])
async def get_backup(backup_key: str):
    """Retrieve a specific backup"""
    try:
        backup_path = os.path.join(settings.LOCAL_BACKUP_DIR, backup_key)
        if not os.path.exists(backup_path):
            raise HTTPException(
                status_code=404,
                detail=f"Backup not found: {backup_key}"
            )

        with open(backup_path, 'r') as f:
            config = yaml.safe_load(f)

        return {
            "status": "success",
            "backup": {
                "filename": backup_key,
                "config": config
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve backup: {str(e)}"
        ) 