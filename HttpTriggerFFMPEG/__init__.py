import logging
import ffmpy
import azure.functions as func
from urllib.parse import unquote
from azure.storage.blob import BlockBlobService
import os
import pyodbc
import pandas as pd
import cv2

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('change 5')

    username = 'matt.shepherd'
    password = os.getenv("sqlPassword")
    driver = '{ODBC Driver 17 for SQL Server}'
    server = "fse-inf-live-uk.database.windows.net"
    database = 'TestDb'    
    connectionString = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
    with pyodbc.connect(connectionString) as conn:
        ## Get SQL table in pandas DataFrame
        df = pd.read_sql(sql="SELECT * FROM doesthiswork",
                            con=conn)
    
    executablePath = df.loc[0,'RawPlayer']
    executeCommands = eval(df.loc[0,'Command'].replace("$","'''"))
    fileURL = df.loc[0,'url']

    # fileURL = "https://fsevideos.blob.core.windows.net/us-office/Bournemouth%20Highlights.mp4"
    fileExt = fileURL.split(".")[-1]
    container = fileURL.split("/")[-2]
    fileName = unquote(fileURL.split("/")[-1])
    fileNameNoSpaces = fileName.replace(" ","")
    connString = "DefaultEndpointsProtocol=https;AccountName=fsevideos;AccountKey=xfYncTDRCowSrISbdsSknM05jqOrJXc4Oavq7BQ56yR7uQ7MCeL5aXmBsbsE+SZ+++xGt2oy6FvrEdpryc+vwQ==;EndpointSuffix=core.windows.net"
    bbs = BlockBlobService(connection_string=connString)

    tempClipFilePath = "/tmp/" + fileNameNoSpaces
    logging.info(f"tempClipFilePath: {tempClipFilePath}")
    bbs.get_blob_to_path(
        container_name=container,
        blob_name=fileName,
        file_path=tempClipFilePath
    )
    logging.info(f"tempClipFilePath exists - {tempClipFilePath} - {os.path.exists(tempClipFilePath)}")
    logging.info("blob downloaded to temp location")
    logging.info(f"os.listdir(): {os.listdir()}")
    logging.info(f"os.listdir('HttpTriggerFFMPEG'): {os.listdir('HttpTriggerFFMPEG')}")
    logging.info(f"executablePath: {executablePath}")
    logging.info(f"os.path.exists(executablePath): {os.path.exists(executablePath)}")
    for ec in executeCommands:
        logging.info(f"executeCommand: {ec}")
        if ec.startswith("EXISTS"):
            e = ec.replace("EXISTS ","")
            logging.info(f"os.path.exists(e):{os.path.exists(e)}")
        else:
            logging.info(f"os.popen(executeCommand).read(): {os.popen(ec).read()}")


    startSeconds = 10
    subclipDurationSeconds = 10
    fileOutPath = "/tmp/middle10seconds" + '.' + fileExt

    ff = ffmpy.FFmpeg(
        ## FFMPEG is in the parent directory
        executable=executablePath,
        inputs={
                tempClipFilePath : f"-ss {startSeconds}"
                },
        outputs={
                fileOutPath : f"-t {subclipDurationSeconds} -c copy"
                }
        )
    logging.info(f"ff.cmd: {ff.cmd}")
    ff.run()

    logging.info("command run")

    for fp in [
        "test",
        "middle10seconds"
    ]:
        logging.info(f"starting {fp} upload")
        fp1 = "/tmp/" + fp + '.' + fileExt
        bbs.create_blob_from_path(
            container_name=container,
            blob_name=fp + '.' + fileExt,
            file_path=fp1
        )
        logging.info(f"{fp} upload done")

    return func.HttpResponse("It worked.")

