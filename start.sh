#!/bin/bash

# Create initial config file if it doesn't exist
mkdir -p /etc/traefik/dynamic
if [ ! -f /etc/traefik/dynamic/config.yaml ]; then
    echo "http:
  routers: {}
  services: {}" > /etc/traefik/dynamic/config.yaml
fi

# Start Traefik in the background
traefik --configfile=/etc/traefik/traefik.yaml &

# Wait a moment for Traefik to initialize
sleep 3

# Start the FastAPI application
python3 -m app.main