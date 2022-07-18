#!/usr/bin/bash

echo '------------------------------------'
echo '|    Starting Integration Test     |'
echo '------------------------------------'

docker-compose up -d

sleep 3

./init_db.sh

sleep 3

docker-compose exec web python manage.py test integration_tests

docker-compose down


echo '------------------------------------'
echo '|        Testing Complete          |'
echo '------------------------------------'
