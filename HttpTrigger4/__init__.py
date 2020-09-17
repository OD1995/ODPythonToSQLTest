import logging
import pyodbc
import pandas as pd
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    server = "fse-inf-live-uk.database.windows.net"
    database = 'AzureCognitive'
    username = 'matt.shepherd'
    # password = os.getenv("sqlPassword")
    password = "4rsenal!PG01"
    driver = '{ODBC Driver 17 for SQL Server}'
    table = 'AzureBlobVideos'
    # connectionString1 = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    # connectionString2 = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password

    # output = ""
    # with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        # with conn.cursor() as cursor:
            # cursor.execute(f"SELECT VideoName, Event FROM {table}")
            # row = cursor.fetchone()
            # while row:
            #     print (str(row[0]) + " " + str(row[1]))
            #     output = ( "VideoName: " + str(row[0]) + ", Event" + str(row[1]))
            #     row = cursor.fetchone()
        df = pd.read_sql(sql=f"SELECT VideoName, Event FROM {table}",
                            con=conn)

    return func.HttpResponse(str(df))