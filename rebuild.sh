#!/bin/bash

docker-compose down

sudo rm -rf data

docker-compose up -d --build

docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

rm .db_init_done

./init_db.sh

docker-compose down
