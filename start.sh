#!/bin/sh

# Load environment variables from .env file
if [ -f "/.env" ]; then
    set -a
    . /.env
    set +a
fi

python3 -m app.main