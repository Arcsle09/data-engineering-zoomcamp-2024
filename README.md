# data-engineering-zoomcamp-2024

Week-1: 01_docker_terraform:

        Learnings so far: 
        - how to ingest the external data to postgres db using python and its libraries.
        - how to spin up postgres db and postgres admin containers and place them in same network.
        - dockerize the parameterized python script and spin up container in the same network where we have postgres db.

        Additional Contribution:
        - Ehnaced the python script to handle multiple data sources with different file formats (gzip and csv) and read the source in csv format.
        - Handling the column data types conversion where ever applicable.
        - Developed the shell script to automate the docker commands for all data ingestion activities.
