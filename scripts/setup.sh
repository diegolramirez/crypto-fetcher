#!/usr/bin/bash

# load PG connection variables from .env
source .env

# setup python environment
python -m venv ./.venv
source ./.venv/bin/activate

# install python packages
pip install -r requirements.txt

# create local data storage and logging directories
mkdir -p data
mkdir -p logs

# setup local postgresql db using docker
docker pull postgres
docker run --name $CONTAINER_NAME \
            -e POSTGRES_USER=$PG_USERNAME \
            -e POSTGRES_PASSWORD=$PG_PASSWORD \
            -e POSTGRES_DB=$PG_DB \
            -d -p $PG_PORT:5432 postgres
until [ "`docker inspect -f {{.State.Running}} $CONTAINER_NAME`"=="true" ]; do
    sleep 1;
done;
sleep 5
docker cp sql/install.sql $CONTAINER_NAME:.
docker exec $CONTAINER_NAME psql -U $PG_USERNAME -d $PG_DB -c "\i install.sql;"
