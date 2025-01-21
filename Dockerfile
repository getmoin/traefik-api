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

COPY app/ ./app/
COPY .env ./.env

RUN mkdir -p /etc/traefik/acme /etc/traefik/backups && \
    chmod +x /usr/local/bin/start.sh && \
    sed -i 's/\r$//' /usr/local/bin/start.sh

EXPOSE 8000

ENTRYPOINT ["sh", "/usr/local/bin/start.sh"]