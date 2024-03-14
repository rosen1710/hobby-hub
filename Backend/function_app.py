import azure.functions as func
import logging
from django.db import models

import User

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="create_user")
def Create_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        email = req_body.get('email')
        password = req_body.get('password')
        fullname = req_body.get('fullname')
        age = req_body.get('age')
        description = req_body.get('description')

    if email and password and fullname and age and description:
        user = User(email, password, fullname, age, description)
        user.save()
        return func.HttpResponse(
            "User added successfully.",
            status_code=200
        )
    else:
        return func.HttpResponse(
             "Not valid data provided!",
             status_code=400
        )