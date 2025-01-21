FROM python:3.9-alpine

RUN apk update && apk add \
    python3 \
    py3-pip \
    gcc \
    python3-dev \
    musl-dev \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY .env ./.env
COPY start.sh /usr/local/bin/
COPY . .

# # Create directories and set permissions
# RUN mkdir -p /etc/traefik/acme /etc/traefik/backups && \
#     chmod +x /usr/local/bin/start.sh && \
#     sed -i 's/\r$//' /usr/local/bin/start.sh

# Create necessary directories and files
RUN mkdir -p /etc/traefik/dynamic && \
    touch /etc/traefik/dynamic/config.yaml && \
    chmod 644 /etc/traefik/dynamic/config.yaml

EXPOSE 8000

# Set the start script as the entrypoint
ENTRYPOINT ["/usr/local/bin/start.sh"]