#!/bin/bash
cd data
FILE=.db_init_done
if [ -f "$FILE" ]; then
    echo "db already initialized... skipping"
else
    cd ../
    docker compose run web python initialize.py
    cd data
    touch .db_init_done
fi