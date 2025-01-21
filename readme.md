## The easiest way to play
```
docker-compose up --build
```

### To build the image
```
docker build -t traefik-manager .
```

### To run the docker container
```
docker run -d \
  -p 80:80 \
  -p 443:443 \
  -p 8080:8080 \
  -p 8000:8000 \
  -v /path/to/dynamic:/etc/traefik/dynamic \
  -v /path/to/backups:/etc/traefik/backups \
  traefik-manager
```

Ports 80 and 443 are required for certificate resolution.
Ports 8080 is for the traefik dashboard
Port 8000 is for the fastapi