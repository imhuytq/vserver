#! /usr/bin/env bash

# Run migrations
alembic upgrade head

# Run server
uvicorn vserver.main:app --host 0.0.0.0 --port 8080
