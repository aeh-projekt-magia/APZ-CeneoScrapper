#!/bin/bash

# This script is used to start the application
echo "<1.> docker compose build"
echo "<2.> docker compose up -d"
echo "<3.> docker compose stop"
echo "<4.> docker compose down"
echo "<5.> docker compose up -d --scale app=5"
echo "<6.> docker exec python manage.py recreate_db"
echo "<7.> docker exec python manage.py create_admin"

read -p "Choose option: " CHOICE

if [ $CHOICE == 1 ]; then
    docker-compose -f ./flask_app/docker-compose.yml build

elif [ $CHOICE == 2 ]; then
    docker-compose -f ./flask_app/docker-compose.yml up -d

elif [ $CHOICE == 3 ]; then
    docker-compose -f ./flask_app/docker-compose.yml stop

elif [ $CHOICE == 4 ]; then
    docker-compose -f ./flask_app/docker-compose.yml down

elif [ $CHOICE == 5 ]; then
    docker-compose -f ./flask_app/docker-compose.yml up -d --scale app=5

elif [ $CHOICE == 6 ]; then
    CONTAINER_ID=$(docker ps -f name=flask_app-app -q -n 1)
    echo "Using container id: $CONTAINER_ID"
    docker exec $CONTAINER_ID python manage.py recreate_db

elif [ $CHOICE == 7 ]; then
    CONTAINER_ID=$(docker ps -f name=flask_app_app -q -n 1)
    echo "Using container id: $CONTAINER_ID"
    unset PASSWORD
    unset EMAIL
    echo -n "Enter email: "
    read EMAIL
    echo -n "Enter password: "
    read -s PASSWORD
    docker exec $CONTAINER_ID python manage.py create_admin --email $EMAIL --password $PASSWORD
else
    echo "Wrong option!"
fi

echo "Done!"
