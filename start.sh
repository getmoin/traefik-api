#!/bin/sh

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Start the FastAPI application
uvicorn app.main:app --host 0.0.0.0 --port 8000



# mkdir -p /etc/traefik/dynamic
# if [ ! -f /etc/traefik/dynamic/config.yaml ]; then
#     echo "http:
#   routers: {}
#   services: {}" > /etc/traefik/dynamic/config.yaml
# fi

# export $(grep -v '^#' .env | xargs)
# traefik --configfile=/etc/traefik/traefik.yaml &

# sleep 3

# python3 -m app.main