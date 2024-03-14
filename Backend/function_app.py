import azure.functions as func
import logging
from django.db import models

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="create_user")
def Create_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        username = req_body.get('username')
        password = req_body.get('password')

    if username and password:
        # Django logic
        return func.HttpResponse(
            "User added successfully.",
            status_code=200
        )
    else:
        return func.HttpResponse(
             "Not valid data provided!",
             status_code=400
        )