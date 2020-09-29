import logging
from azure.storage.blob import BlockBlobService

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    ## Create BlockBlobService
    connectionStringOutput = "DefaultEndpointsProtocol=https;AccountName=fsevideos;AccountKey=xfYncTDRCowSrISbdsSknM05jqOrJXc4Oavq7BQ56yR7uQ7MCeL5aXmBsbsE+SZ+++xGt2oy6FvrEdpryc+vwQ==;EndpointSuffix=core.windows.net"
    block_blob_service = BlockBlobService(connection_string=connectionStringOutput)
    logging.info(f'BlockBlobService created for account "{block_blob_service.account_name}"')
    ## Create some text to upload to the blob storage account
    s = "some test letters"
    logging.info(f"About to create txt file containing '{s}'")
    ## Create blob
    block_blob_service.create_blob_from_text(container_name="us-office",
                                                blob_name=s,
                                                text="test.txt")
    logging.info("Blob created")
    return func.HttpResponse(str(s))
