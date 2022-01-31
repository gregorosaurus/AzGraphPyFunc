import logging

import azure.functions as func
import json
from services.graphapi import GraphAPI
import msal

graphAPI = GraphAPI()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Calling Get Users.')

    global graphAPI
    graphAPI.authenticate()
    users = graphAPI.get_users()

    return func.HttpResponse(json.dumps(users, indent=4))
