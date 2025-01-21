#!/bin/sh

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

python3 -m app.main