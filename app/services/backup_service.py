import boto3
import os
import traceback
from fastapi import HTTPException
from botocore.exceptions import ClientError
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
            print(f"Starting S3 backup process...")
            print(f"Using bucket: {settings.S3_BUCKET_NAME}")
            print(f"Using region: {settings.AWS_REGION}")
            
            # Test bucket access
            try:
                print("Testing bucket access...")
                s3_client.head_bucket(Bucket=settings.S3_BUCKET_NAME)
                print("Bucket access successful")
            except ClientError as e:
                print(f"Bucket access error: {str(e)}")
                error_code = e.response.get('Error', {}).get('Code', 'Unknown')
                print(f"Error code: {error_code}")
                raise

            backup_key = f"traefik-backups/{backup_filename}"
            print(f"Preparing to upload file: {backup_key}")
            
            # Debug file content and existence
            try:
                with open(settings.CONFIG_FILE, 'rb') as file:
                    content = file.read()
                    print(f"File size to upload: {len(content)} bytes")
                    
                    print("Attempting S3 upload...")
                    s3_client.upload_fileobj(
                        file, 
                        settings.S3_BUCKET_NAME, 
                        backup_key,
                        ExtraArgs={
                            'ContentType': 'application/yaml'
                        }
                    )
                    print("Upload completed")
            except IOError as e:
                print(f"File read error: {str(e)}")
                raise
            except ClientError as e:
                print(f"S3 upload error: {str(e)}")
                error_code = e.response.get('Error', {}).get('Code', 'Unknown')
                print(f"Error code: {error_code}")
                raise
            
            # Verify upload
            try:
                print("Verifying upload...")
                s3_client.head_object(
                    Bucket=settings.S3_BUCKET_NAME,
                    Key=backup_key
                )
                print("Upload verified successfully")
                
                return ConfigBackup(
                    backup_key=backup_key,
                    timestamp=timestamp,
                    location='s3'
                )
            except ClientError as e:
                print(f"Upload verification failed: {str(e)}")
                error_code = e.response.get('Error', {}).get('Code', 'Unknown')
                print(f"Error code: {error_code}")
                raise
                
        except Exception as e:
            print(f"S3 backup failed with exception: {str(e)}")
            print("Full traceback:")
            traceback.print_exc()
            
            # Print boto3 client configuration (without credentials)
            if s3_client:
                client_config = s3_client._client_config
                print(f"S3 Client Configuration:")
                print(f"Region: {client_config.region_name}")
                print(f"Endpoint URL: {client_config.endpoint_url}")
                print(f"Verify SSL: {client_config.verify}")
    
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