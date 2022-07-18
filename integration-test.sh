#!/usr/bin/bash

echo '------------------------------------'
echo '|    Starting Integration Test     |'
echo '------------------------------------'

docker-compose up -d

sleep 3

#./init_db.sh

sleep 3

echo ' '
echo '------------------------------------'
echo '|        Testing Company 2          |'
echo '------------------------------------'
echo ' '
echo ' '

curl http://localhost:8000/schedule/2022/FALL/2

echo ' '
echo ' '
echo ' '
echo '------------------------------------'
echo '|        Testing Company 1          |'
echo '------------------------------------'
echo ' '
echo ' '
echo ' '

curl http://localhost:8000/schedule/2022/FALL/1


echo ' '
echo ' '
echo ' '
echo '------------------------------------'
echo '|        Testing Complete          |'
echo '------------------------------------'
echo ' '
echo ' '
echo ' '

docker-compose down