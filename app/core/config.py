import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # AWS Settings
    AWS_REGION: str = os.getenv("AWS_REGION")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    ENABLE_S3_BACKUP: bool = os.getenv("ENABLE_S3_BACKUP", "false").lower() == "true"
    
    # Traefik Settings
    CONFIG_FILE: str = os.getenv("CONFIG_FILE", "/etc/traefik/dynamic/config.yaml")
    LOCAL_BACKUP_DIR: str = os.getenv("LOCAL_BACKUP_DIR", "/etc/traefik/backups")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME")
    
    # Certificate Settings
    CERT_RESOLVER: str = os.getenv("CERT_RESOLVER", "acmeresolver")
    AWS_HOSTED_ZONE_ID: str = os.getenv("AWS_HOSTED_ZONE_ID")
    AWS_CERT_EMAIL: str = os.getenv("AWS_CERT_EMAIL")

settings = Settings() 