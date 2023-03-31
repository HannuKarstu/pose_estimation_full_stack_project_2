#!/bin/bash

FILE=my_env.env

if [ -f "$FILE" ]; then
    set -a
    source $FILE
    docker compose -f docker-compose.prod.yml build
    docker compose -f docker-compose.prod.yml push
else 
    echo "$FILE does not exist. Create the file and add REPOSITORY=<REPOSITORY=<your Docker Hub repository> to it."
fi