#!/bin/bash

mkdir -p /etc/traefik/dynamic
if [ ! -f /etc/traefik/dynamic/config.yaml ]; then
    echo "http:
  routers: {}
  services: {}" > /etc/traefik/dynamic/config.yaml
fi

traefik --configfile=/etc/traefik/traefik.yaml &

sleep 3

python3 -m app.main