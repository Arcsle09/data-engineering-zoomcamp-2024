#!/usr/bin/env bash

read -p "provide the container name for data ingestion: " container_name

echo "searching the network of database services...."

network_id=$(docker network ls -f NAME="2_docker_sql_default" --format "{{.ID}}")

echo "network id for database host is $network_id"

echo "Ingestion started.."

docker build -t $container_name:final_version .

docker run -it \
    --network=$network_id \
    $container_name:final_version \
    --user=root \
    --password=root \
    --host=pd-database \
    --port=5432 \
    --db_name=ny_taxi \
    --table-name=yellow_taxi_data \
    --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"\
    --filename="yellow_tripdata.csv"


docker run -it \
    --network=$network_id \
    $container_name:final_version \
    --user=root \
    --password=root \
    --host=pd-database \
    --port=5432 \
    --db_name=ny_taxi \
    --table-name=taxi_zone_lookup \
    --url="https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"\
    --filename="taxi_zone_lookup.csv"

echo "Ingestion Ended..."
