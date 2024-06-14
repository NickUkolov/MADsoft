#!/bin/bash
while true; do
    echo "RUN - alembic upgrade head"
    alembic upgrade head
    if [[ "$?" == "0" ]]; then
        echo "Exit code - 0"
        break
    fi
    echo "Exit code != 0"
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done

exec uvicorn --host=0.0.0.0 --port="$API_PORT" --log-level debug main:app