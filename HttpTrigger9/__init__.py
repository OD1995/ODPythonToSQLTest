import logging
from azure.storage.blob import BlockBlobService
import requests
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    ## Create BlockBlobService
    connectionStringOutput = "DefaultEndpointsProtocol=https;AccountName=fsevideos;AccountKey=xfYncTDRCowSrISbdsSknM05jqOrJXc4Oavq7BQ56yR7uQ7MCeL5aXmBsbsE+SZ+++xGt2oy6FvrEdpryc+vwQ==;EndpointSuffix=core.windows.net"
    block_blob_service = BlockBlobService(connection_string=connectionStringOutput)
    logging.info(f'BlockBlobService created for account "{block_blob_service.account_name}"')
    ## Get bytes for image
    imageURL = "https://lasportshub.com/wp-content/uploads/getty-images/2020/03/1196569592.jpeg"
    # imageBytes = base64.b64encode(requests.get(imageURL).content)
    r = requests.get(imageURL,stream=True)
    logging.info(f"About to create jpeg file from '{imageURL}'")
    # logging.info(f"Variable type: {type(imageBytes)}")
    ## Create blob
    block_blob_service.create_blob_from_bytes(container_name="us-office",
                                                blob_name="jared goff.jpeg",
                                                blob=r.content)
    logging.info("Blob created")
    return func.HttpResponse(body=imageURL)