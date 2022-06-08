#!/bin/bash


docker-compose up -d --build && docker-compose exec web python manage.py test 
docker-compose down 

echo "TESTING COMPLETE"
