#!/bin/bash
exec uvicorn --host=0.0.0.0 --port="$MEDIA_SERVICE_PORT" --log-level debug main:app