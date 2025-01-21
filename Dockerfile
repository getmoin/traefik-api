FROM alpine:latest

# Install required packages
RUN apk add --no-cache python3 py3-pip py3-virtualenv

# Create necessary directories and files
RUN mkdir -p /etc/traefik/dynamic /etc/traefik/acme /etc/traefik/backups && \
    touch /etc/traefik/dynamic/config.yaml && \
    chmod 644 /etc/traefik/dynamic/config.yaml

# Create app directory
WORKDIR /app

# Create and activate virtual environment
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the start script first
COPY start.sh /usr/local/bin/

# Set proper permissions and fix line endings
RUN chmod 755 /usr/local/bin/start.sh && \
    sed -i 's/\r$//' /usr/local/bin/start.sh

# Copy the rest of the application
COPY . .

# Set the start script as the entrypoint
ENTRYPOINT ["/usr/local/bin/start.sh"]