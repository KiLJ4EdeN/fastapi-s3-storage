#!/bin/bash

gunicorn object_storage.api:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers "${APP_WORKERS}"
