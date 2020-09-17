import logging
import pyodbc
import pandas as pd
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    server = "fse-inf-live-uk.database.windows.net"
    database = 'AzureCognitive'
    username = 'matt.shepherd'
    password = "4rsenal!PG01"
    driver = '{ODBC Driver 17 for SQL Server}'
    table = 'AzureBlobVideos'

    output = ""
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        df = pd.read_sql(sql=f"SELECT VideoName, Event FROM {table}",
                            con=conn)

    return func.HttpResponse(str(df))