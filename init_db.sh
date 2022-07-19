#!/bin/bash

FILE=.db_init_done
if [ -f "$FILE" ]; then
    echo "db already initialized... skipping"
else
    docker compose run web python initialize.py
    touch .db_init_done
fi