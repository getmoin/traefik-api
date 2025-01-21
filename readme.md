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

Here port 80 and 443 are required for certificate resolution.
8080 is for the traefik dashboard
8000 is for the fastapi