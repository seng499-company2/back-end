#!/bin/bash


docker-compose up -d  && docker-compose exec web python manage.py test
docker-compose down


echo "TESTING COMPLETE"
