import boto3
import os
from fastapi import HTTPException
from app.core.config import settings
from app.core.models import ConfigBackup

s3_client = None
if settings.ENABLE_S3_BACKUP:
    try:
        s3_client = boto3.client(
            's3',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
    except Exception as e:
        print(f"Warning: Failed to initialize S3 client: {str(e)}")

def create_backup(timestamp: str) -> ConfigBackup:
    """Create backup in S3 or locally"""
    backup_filename = f"traefik-config_{timestamp}.yaml"
    
    # Try S3 if enabled and configured
    if settings.ENABLE_S3_BACKUP and s3_client:
        try:
            backup_key = f"traefik-backups/{backup_filename}"
            with open(settings.CONFIG_FILE, 'rb') as file:
                s3_client.upload_fileobj(file, settings.S3_BUCKET_NAME, backup_key)
            return ConfigBackup(
                backup_key=backup_key,
                timestamp=timestamp,
                location='s3'
            )
        except Exception as e:
            print(f"S3 backup failed: {str(e)}")
    
    # Local backup
    try:
        os.makedirs(settings.LOCAL_BACKUP_DIR, exist_ok=True)
        backup_path = os.path.join(settings.LOCAL_BACKUP_DIR, backup_filename)
        with open(settings.CONFIG_FILE, 'rb') as src, open(backup_path, 'wb') as dst:
            dst.write(src.read())
        return ConfigBackup(
            backup_key=backup_path,
            timestamp=timestamp,
            location='local'
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Backup failed: {str(e)}"
        )