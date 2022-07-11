#!/bin/bash


docker-compose up -d  && docker-compose exec web python manage.py test schedule
docker-compose down


echo "TESTING COMPLETE"
