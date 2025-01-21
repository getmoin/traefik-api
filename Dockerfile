FROM traefik:v2.10

# Install Python and dependencies
USER root
RUN apk update && apk add \
    python3 \
    py3-pip \
    gcc \
    python3-dev \
    musl-dev \
    && rm -rf /var/cache/apk/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code and configuration
COPY app/ ./app/
COPY traefik.yaml /etc/traefik/traefik.yaml
COPY config.yaml /etc/traefik/dynamic/config.yaml
COPY start.sh /usr/local/bin/start.sh

# Create necessary directories
RUN mkdir -p /etc/traefik/acme /etc/traefik/backups && \
    chmod +x /usr/local/bin/start.sh && \
    sed -i 's/\r$//' /usr/local/bin/start.sh

# Expose ports for Traefik and API
EXPOSE 80 443 8000 8080

# Override the default entrypoint
ENTRYPOINT ["sh", "/usr/local/bin/start.sh"]