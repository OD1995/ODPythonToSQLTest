import logging
import cv2
import math
from datetime import datetime
import json
import tempfile
from azure.storage.blob import BlockBlobService
import sys
import os
sys.path.append(os.path.abspath('.'))
import MyClasses
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    ## Get blob details
    fileURL = "https://fsevideos.blob.core.windows.net/us-office/Brighton Highlights.mp4"
    container = "us-office"
    fileName = "Brighton Highlights.mp4"
    timeToCutStr = "2095-03-13 00:00:00.00000"
    timeToCut = datetime.strptime(timeToCutStr,
                                    "%Y-%m-%d %H:%M:%S.%f")
    logging.info(f"fileURL: {fileURL}")
    logging.info(f"container: {container}")
    logging.info(f"fileName: {fileName}")
    logging.info(f"timeToCutStr: {timeToCutStr}")
    ## Open the video
    vidcap = cv2.VideoCapture(fileURL)
    logging.info(f"VideoCapture object created for {fileURL}")
    success,image = vidcap.read()
    ## Get metadata
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frameCount = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    logging.info('Video metadata acquired')
    logging.info(f"frameCount: {str(frameCount)}")

    ## If frame count negative, download locally and try again
    if frameCount <= 0:
        logging.info("Frame count greater than 0, so local download needed")
        with tempfile.TemporaryDirectory() as dirpath:
            ## Get blob and save to local directory
            vidLocalPath = fr"{dirpath}\{fileName}"
            # logging.info("About to get connection string")
            # logging.info(f"CS: {os.environ['fsevideosConnectionString']}")
            fsevideosConnectionString = "DefaultEndpointsProtocol=https;AccountName=fsevideos;AccountKey=xfYncTDRCowSrISbdsSknM05jqOrJXc4Oavq7BQ56yR7uQ7MCeL5aXmBsbsE+SZ+++xGt2oy6FvrEdpryc+vwQ==;EndpointSuffix=core.windows.net"
            logging.info("About to create BlockBlobService")
            block_blob_service = BlockBlobService(connection_string=fsevideosConnectionString)
            logging.info("BlockBlobService created")
            block_blob_service.get_blob_to_path(container_name=container,
                                                blob_name=fileName,
                                                file_path=vidLocalPath)
            logging.info("Blob saved to path")
            with MyClasses.MyVideoCapture(vidLocalPath) as vc1:
                frameCount = int(vc1.get(cv2.CAP_PROP_FRAME_COUNT))

            logging.info(f"(new) frameCount: {str(frameCount)}")
    ## Get number of frames wanted per second
    wantedFPS = 1
    takeEveryN = math.floor(fps/wantedFPS)
    if timeToCutStr != "2095-03-13 00:00:00.00000":
        ## Work out when the recording starts based on the filename
        vidName = fileName.split("\\")[-1].replace(".mp4","")
        vidName1 = vidName[:vidName.index("-")]
        recordingStart = datetime.strptime(f'{vidName1.split("_")[0]} {vidName1[-4:]}',
                                            "%Y%m%d %H%M")
        ## Work out which frames to reject
        frameToCutFrom = int((timeToCut - recordingStart).seconds * fps)
    else:
        ## If last play is my 100th birthday, set a huge number that it'll never reach
        frameToCutFrom = 1000000000
    logging.info("List of frame numbers about to be generated")
    ## Create list of frame numbers to be JPEGed
    listOfFrameNumbers = [i
                            for i in range(frameCount)
                            if (i % takeEveryN == 0) & (i <= frameToCutFrom)]
    logging.info(f"listOfFrameNumbers created with {len(listOfFrameNumbers)} elements")
    return func.HttpResponse(json.dumps(listOfFrameNumbers))