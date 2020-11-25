import logging
import json

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    #starter: str

    returnMe = {}
    try:
        A = req.get_body().decode("utf-8")
        A1 = json.dumps(A)
        returnMe['body'] = A
        logging.info("body retrieved")
    except Exception as e:
        logging.info(e)

    try:
        B = req.get_json()
        B1 = json.dumps(B)
        returnMe['json'] = B
        logging.info("json retrieved")
    except Exception as e:
        logging.info(e)

    try:
        C = req.params
        C0 = dict(C)
        C1 = json.dumps(C0)
        returnMe['params'] = C0
        logging.info("params retrieved")
    except Exception as e:
        logging.info(e)

    try:
        D = req.route_params
        D0 = dict(D)
        D1 = json.dumps(D0)
        returnMe['route_params'] = D0
        logging.info("route_params retrieved")
    except Exception as e:
        logging.info(e)

    for f in [  
                'fileUrl',
                'container',
                'blob'
                ]:
        try:
            returnMe[f] = req.params.get(f)
        except:
            logging.info(f"{f} didn't work")

    if len(returnMe) == 0:
        returnMe = {'Nothing' : 'Worked'}

    return func.HttpResponse(json.dumps(returnMe))
    # logging.info('Python HTTP trigger function processed a request.')

    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')

    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #         req_body,
    #          status_code=200
    #     )
