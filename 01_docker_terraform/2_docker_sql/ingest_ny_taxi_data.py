import pandas as pd
from sqlalchemy import create_engine
import time
import argparse
import os

def main(params):
    
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db_name = params.db_name
    table_name = params.table_name
    url = params.url
    csv_name = params.filename
    
    if url.endswith('.gz'):    
        wget_gzip_chained_command = f"wget -O - {url} > ny_taxi_2021_data.gz"
        
        os.system(wget_gzip_chained_command)
        
        time.sleep(2)
        
        os.system(f"gzip -c -d ny_taxi_2021_data.gz > {csv_name}")
        
        time.sleep(2)
        
    if url.endswith('.csv'):
        wget_gzip_chained_command = f"wget -O - {url} > {csv_name}"
        
        os.system(wget_gzip_chained_command)
        
        
    df_iter = pd.read_csv(csv_name,
                    chunksize=100000,
                    iterator=True)
    
    df = next(df_iter)
    
    if 'tpep_pickup_datetime' in df.columns:
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    
    if 'tpep_dropoff_datetime' in df.columns:
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    pg_sql_engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db_name}")

    df.head(0).to_sql(name=table_name,con=pg_sql_engine,if_exists='replace',index=False)
    
    t_start = time.time()
    
    df.to_sql(name=table_name,con=pg_sql_engine,if_exists='append',index=False)
    
    t_end = time.time()
    
    print('Inserted first chunk....took %.3f seconds' %(t_end - t_start))

    while  True:
        try:    
            t_start = time.time()

            df_next = next(df_iter)

            df_next.to_sql(name=table_name,con=pg_sql_engine,if_exists='append',index=False)

            t_end = time.time()

            print('Inserted another chunk.... took %.3f seconds' %(t_end - t_start))
            
        except StopIteration:
            print("The data ingestion is successfully completed.")
            break
        
if __name__ == "__main__":    
    
    parser = argparse.ArgumentParser(description='Ingest NY Taxi Data to PostgresDB')
    
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='hostname for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db_name', help='database name for postgres')
    parser.add_argument('--table-name', help='table name for postgres')
    parser.add_argument('--url', help='url of the external data source')
    parser.add_argument('--filename', help='filename to be stored')
    args = parser.parse_args()
    
    main(args)



