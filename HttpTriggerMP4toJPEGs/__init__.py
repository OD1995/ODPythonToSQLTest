import logging
import cv2
from azure.storage.blob import BlockBlobService
import re
import azure.functions as func

def getContainerAndConnString(sport,
                                container):
    """
    Using the sport value from the AzureBlobVideos SQL table and
    the container the MP4 is currently in, work out which container
    and blob storage account to insert images into
    """
    ## # Make some adjustments to make the container name as ready as possible
    ## Convert all `sport` characters to lower case
    if sport is not None:
        isNotNone = True
        _sport_ = "".join([x.lower() if isinstance(x,str)
                            else "" if x == " " else x
                            for x in sport])
        ## Replace double hyphens
        _sport_ = _sport_.replace("--","-").replace("--","-")

        ## # Make some checks
        ## Check that the length is between 3 and 63 charachters
        length = (len(_sport_) >= 3) & (len(_sport_) <= 63)
        ## Check that all characters are either a-z, 0-9 or -
        rightCharTypes = True if re.match("^[a-z0-9-]*$", _sport_) else False
        ## Check that the first character is either a-z or 0-9
        firstCharRight = True if re.match("^[a-z0-9]*$", _sport_[0]) else False
        ## Check that the last character is either a-z or 0-9
        lastCharRight = True if re.match("^[a-z0-9]*$", _sport_[-1]) else False
    else:
        isNotNone = False
        length = False
        rightCharTypes = False
        firstCharRight = False
        lastCharRight = False
        _sport_ = ""



    if isNotNone & length & rightCharTypes & firstCharRight & lastCharRight:
        return  _sport_,"DefaultEndpointsProtocol=https;AccountName=fsecustomvisionimages;AccountKey=0gbOTBrl68MCGXlu6vHRK6DyQOIjRI5HRgTmfReCDW2cTmUnkCITP7DBRme9zI2yRsdWOrPxkDdz3v8Ti5Q3Zw==;EndpointSuffix=core.windows.net"
    else:
        return container,"DefaultEndpointsProtocol=https;AccountName=fsevideos;AccountKey=xfYncTDRCowSrISbdsSknM05jqOrJXc4Oavq7BQ56yR7uQ7MCeL5aXmBsbsE+SZ+++xGt2oy6FvrEdpryc+vwQ==;EndpointSuffix=core.windows.net"


def main(req: func.HttpRequest) -> func.HttpResponse:
    ## Get blob details
    fileURL = "https://fsevideos.blob.core.windows.net/us-office/Brighton Highlights.mp4"
    container = "us-office"
    fileName = "Brighton Highlights.mp4"
    sport = None
    event = None
    frameNumberList = [x for x in range(0,775,25)]
    logging.info(f"frameNumberList (type: {type(frameNumberList)}, length: {len(frameNumberList)}) received")
    # ## Get clean video name to be used as folder name (without ".mp4" on the end)
    # vidName = MyFunctions.cleanUpVidName(fileName.split("/")[-1])[:-4]
    ## Return the container name and connection string to insert images into
    containerOutput, connectionStringOutput = getContainerAndConnString(
                                                        sport,
                                                        container
                                                        )
    logging.info(f"containerOutput: {containerOutput}")
    logging.info(f"connectionStringOutput: {connectionStringOutput}")
    ## Set the file name to be used
    if event is not None:
        fileNameFolder = event
    else:
        ## Blob name without ".mp4"
        fileNameFolder = fileName.split("/")[-1][:-4]
    logging.info(f"fileNameFolder: {fileNameFolder}")
    ## Create BlockBlobService object to be used to upload blob to container
    block_blob_service = BlockBlobService(connection_string=connectionStringOutput)
    logging.info(f'BlockBlobService created for account "{block_blob_service.account_name}"')
    # Get names of all containers in the blob storage account
    containerNames = [x.name
                        for x in block_blob_service.list_containers()]
    ## Create container (will do nothing if container already exists)
    if containerOutput not in containerNames:
        existsAlready = block_blob_service.create_container(container_name=containerOutput,
                                                            fail_on_exist=False)
        logging.info(f"Container '{containerOutput}' didn't exist, now has been created")
    else:
        logging.info(f"Container '{containerOutput}' exists already'")
    ## Open the video
    vidcap = cv2.VideoCapture(fileURL)
    logging.info("VideoCapture object created")
    ## Loop through the frame numbers
    # frameNumberName = 1
    # frameNumber = frameNumberList[0]
    for frameNumberName,frameNumber in enumerate(frameNumberList[:2],1):
        ## Create path to save image to
        frameName = (5 - len(str(frameNumberName)))*"0" + str(frameNumberName)
        imagePath = fr"{fileNameFolder}\{frameName}.jpeg"
        ## Set the video to the correct frame
        vidcap.set(cv2.CAP_PROP_POS_FRAMES,
                    frameNumber)
        logging.info(f"Video set to frame number: {frameNumber}")
        ## Create the image
        success,image = vidcap.read()
        logging.info(f"Image read, success: {success}, `image` type: {type(image)}")
        if success:
            ## Encode image
            success2, image2 = cv2.imencode(".jpeg", image)
            logging.info(f"Image encoded, success2: {success2}, `image2` type: {type(image2)}")
            if success2:
                ## Convert image2 (numpy.ndarray) to bytes
                byte_im = image2.tobytes()
                logging.info("Image converted to bytes")
                ## Create the new blob
                block_blob_service.create_blob_from_bytes(container_name=containerOutput,
                                                            blob_name=imagePath,
                                                            blob=byte_im)
                logging.info(f"Blob ({imagePath}) created....")
    # for frameNumberName,frameNumber in enumerate(frameNumberList,1):
    #     ## Create path to save image to
    #     frameName = (5 - len(str(frameNumberName)))*"0" + str(frameNumberName)
    #     imagePath = fr"{fileNameFolder}\{frameName}.jpeg"
    #     ## Set the video to the correct frame
    #     vidcap.set(cv2.CAP_PROP_POS_FRAMES,
    #                 frameNumber)
    #     ## Create the image
    #     success,image = vidcap.read()
    #     if success:
    #         ## Encode image
    #         success2, image2 = cv2.imencode(".jpeg", image)
    #         if success2:
    #             ## Convert image2 (numpy.ndarray) to bytes
    #             byte_im = image2.tobytes() 
    #             ## Create the new blob
    #             block_blob_service.create_blob_from_bytes(container_name=containerOutput,
    #                                                         blob_name=imagePath,
    #                                                         blob=byte_im)
    # logging.info("Finished looping through frames")
    return func.HttpResponse("I think it worked")