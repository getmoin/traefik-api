import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from app.core.config import settings
import yaml
import io
import os
from fastapi import HTTPException
from app.core.models import ConfigBackup

def get_s3_client():
    try:
        config = Config(
            region_name='ca-central-1',
            retries={'max_attempts': 3, 'mode': 'standard'},
            s3={'addressing_style': 'virtual'}
        )
        
        client_kwargs = {
            'service_name': 's3',
            'region_name': 'ca-central-1',
            'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY,
            'config': config,
            'endpoint_url': f'https://s3.ca-central-1.amazonaws.com'
        }
        
        return boto3.client(**client_kwargs)
    except Exception:
        return None

s3_client = get_s3_client()

def create_backup(timestamp: str) -> ConfigBackup:
    """Create backup in S3 or locally"""
    backup_filename = f"traefik-config_{timestamp}.yaml"
    
    # Try S3 if enabled and configured
    if settings.ENABLE_S3_BACKUP and s3_client:
        try:
            s3_client.head_bucket(Bucket=settings.S3_BUCKET_NAME)
            backup_key = f"traefik-backups/{backup_filename}"
            
            # Read and prepare the config file
            with open(settings.CONFIG_FILE, 'r') as file:
                config_data = yaml.safe_load(file)
            
            config_yaml = yaml.dump(config_data, default_flow_style=False)
            config_bytes = io.BytesIO(config_yaml.encode('utf-8'))
            
            s3_client.upload_fileobj(
                config_bytes,
                settings.S3_BUCKET_NAME,
                backup_key,
                ExtraArgs={'ContentType': 'application/yaml'}
            )
            
            # Create local backup
            os.makedirs(settings.LOCAL_BACKUP_DIR, exist_ok=True)
            local_backup_path = os.path.join(settings.LOCAL_BACKUP_DIR, backup_filename)
            with open(local_backup_path, 'w') as f:
                f.write(config_yaml)
            
            return ConfigBackup(
                backup_key=backup_key,
                timestamp=timestamp,
                location='s3'
            )
                
        except Exception:
            pass
    
    # If S3 backup failed or was not enabled, create local backup only
    try:
        os.makedirs(settings.LOCAL_BACKUP_DIR, exist_ok=True)
        local_backup_path = os.path.join(settings.LOCAL_BACKUP_DIR, backup_filename)
        
        with open(settings.CONFIG_FILE, 'r') as src:
            config_data = yaml.safe_load(src)
        
        with open(local_backup_path, 'w') as dst:
            yaml.dump(config_data, dst, default_flow_style=False)
        
        return ConfigBackup(
            backup_key=local_backup_path,
            timestamp=timestamp,
            location='local'
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Backup failed: {str(e)}"
        )