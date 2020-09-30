import logging
import json
import pandas as pd
import pyodbc
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("getAzureBlobVideos started")
    ## Get information used to create connection string
    username = 'matt.shepherd'
    # password = os.getenv("sqlPassword")
    password = "4rsenal!PG01"
    driver = '{ODBC Driver 17 for SQL Server}'
    # server = os.getenv("sqlServer")
    server = "fse-inf-live-uk.database.windows.net"
    database = 'AzureCognitive'
    table = 'AzureBlobVideos'
    ## Create connection string
    connectionString = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    logging.info(f'Connection string created: {connectionString}')
    ## Create SQL query to use
    sqlQuery = f"SELECT * FROM {table}"
    with pyodbc.connect(connectionString) as conn:
        ## Get SQL table in pandas DataFrame
        df = pd.read_sql(sql=sqlQuery,
                            con=conn)
    logging.info(f"Dataframe with shape {df.shape} received")
    ## Dict - VideoName : (Sport,Event) 
    dfDict = {vn : (s,e)
                for vn,s,e in zip(df.VideoName,
                                    df.Sport,
                                    df.Event)}
    return func.HttpResponse(json.dumps(dfDict))
