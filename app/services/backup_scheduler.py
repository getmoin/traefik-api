from datetime import datetime
import asyncio
import boto3
import os
from app.api.backup import create_config_backup
from app.core.config import settings

async def upload_to_s3(backup_info):
    """Upload backup file to S3"""
    if settings.ENABLE_S3_BACKUP:
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            
            s3_key = f"backups/{backup_info['backup']['filename']}"
            s3_client.upload_file(
                backup_info['backup']['path'],
                settings.S3_BUCKET_NAME,
                s3_key
            )
            print(f"Backup uploaded to S3: {s3_key}")
            return True
        except Exception as e:
            print(f"Failed to upload backup to S3: {str(e)}")
            return False
    return False

async def schedule_backups():
    """Schedule automatic backups every 3 days"""
    while True:
        try:
            # Use the existing create_config_backup function
            backup_result = await create_config_backup()
            
            if backup_result["status"] == "success":
                print(f"Scheduled backup created: {backup_result['backup']['filename']}")
                
                # Upload to S3 if enabled
                if settings.ENABLE_S3_BACKUP:
                    s3_result = await upload_to_s3(backup_result)
                    if s3_result:
                        print("Backup successfully uploaded to S3")
                    else:
                        print("Failed to upload backup to S3")
            else:
                print("Failed to create scheduled backup")
                
        except Exception as e:
            print(f"Error in backup scheduler: {str(e)}")
        
        # Wait for 3 days (in seconds)
        await asyncio.sleep(3 * 24 * 60 * 60)  # 3 days * 24 hours * 60 minutes * 60 seconds 