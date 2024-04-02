import azure.functions as func
import logging

import bcrypt
import json
import os
import re
from datetime import timedelta
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import sqlalchemy.exc

from models import *

def create_db_engine():
    return create_engine(os.environ['POSTGRESQLCONNSTR_DB_CONNECTION_STRING'])

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="create_tables")
def create_tables(req: func.HttpRequest) -> func.HttpResponse:
    try:
        engine = create_db_engine()

        Base.metadata.create_all(engine)

        return func.HttpResponse(
            json.dumps({
                "message": "Tables were created successfully or already exist"
            }),
            status_code=200
        )
    except Exception as e:
        logging.exception(f"{str(type(e))}: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "exception": str(type(e)),
                "message": str(e)
            }),
            status_code=400
        )

@app.route(route="create_user")
def create_user(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        email = req_body.get('email')
        password = req_body.get('password')
        fullname = req_body.get('fullname')
        age = req_body.get('age')
        description = req_body.get('description')

        emailregex = re.compile(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
        passwordregex = re.compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")
        fullnameregex = re.compile(r"[A-Za-z]{2,25}\s[A-Za-z]{2,25}")

        if not re.fullmatch(emailregex, email):
            raise ValueError("Email is not valid!")

        if not re.fullmatch(passwordregex, password):
            raise ValueError("Password is not valid!")

        if not re.fullmatch(fullnameregex, fullname):
            raise ValueError("Full name is not valid!")

        if (age < 14) or (age > 150):
            raise ValueError("Age is not valid!")

        engine = create_db_engine()

        with Session(engine) as session:
            session.add(
                User(
                    email=email,
                    password=password,
                    fullname=fullname,
                    age=age,
                    description=description
                )
            )
            session.commit()

        return func.HttpResponse(
            json.dumps({
                "message": "User was added successfully"
            }),
            status_code=200
        )
    except sqlalchemy.exc.IntegrityError:
        return func.HttpResponse(
            json.dumps({
                "message": "User with this email already exists!"
            }),
            status_code=400
        )
    except Exception as e:
        logging.exception(f"{str(type(e))}: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "exception": str(type(e)),
                "message": str(e)
            }),
            status_code=400
        )

@app.route(route="create_hobby")
def create_hobby(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        name = req_body.get('name')

        if name == "":
            raise ValueError ("Not a valid name!")

        engine = create_db_engine()

        with Session(engine) as session:
            session.add(
                Hobby(
                    name=name
                )
            )
            session.commit()

        return func.HttpResponse(
            json.dumps({
                "message": "Hobby was added successfully"
            }),
            status_code=200
        )
    except sqlalchemy.exc.IntegrityError:
        return func.HttpResponse(
            json.dumps({
                "message": "This hobby already exists!"
            }),
            status_code=400
        )
    except Exception as e:
        logging.exception(f"{str(type(e))}: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "exception": str(type(e)),
                "message": str(e)
            }),
            status_code=400
        )

@app.route(route="create_channel")
def create_channel(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        name = req_body.get('name')
        hobby_id = req_body.get('hobby_id')

        if name == "":
            raise ValueError ("Not a valid name!")

        engine = create_db_engine()

        with Session(engine) as session:
            hobby = session.scalar(select(Hobby).where(Hobby.id == hobby_id))
            if hobby is None:
                raise ValueError("Hobby with this id does not exist!")
            session.add(
                Channel(
                    name=name,
                    hobby_id=hobby_id
                )
            )
            session.commit()

        return func.HttpResponse(
            json.dumps({
                "message": "Channel was added successfully"
            }),
            status_code=200
        )
    except Exception as e:
        logging.exception(f"{str(type(e))}: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "exception": str(type(e)),
                "message": str(e)
            }),
            status_code=400
        )

@app.route(route="create_message")
def create_message(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        text = req_body.get('text')
        user_id = req_body.get('user_id')
        password = req_body.get('password')
        channel_id = req_body.get('channel_id')

        if text == "":
            raise ValueError ("You can't send an empty message!")

        engine = create_db_engine()

        with Session(engine) as session:
            user = session.scalar(select(User).where(User.id == user_id))

            if user is None:
                raise ValueError("User with this id does not exist!")

            if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
                raise Exception("Wrong password provided!")

            channel = session.scalar(select(Channel).where(Channel.id == channel_id))

            if channel is None:
                raise ValueError("Channel with this id does not exist!")

            session.add(
                Message(
                    text=text,
                    user_id=user_id,
                    channel_id=channel_id
                )
            )
            session.commit()

        return func.HttpResponse(
            json.dumps({
                "message": "Message was added successfully"
            }),
            status_code=200
        )
    except Exception as e:
        logging.exception(f"{str(type(e))}: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "exception": str(type(e)),
                "message": str(e)
            }),
            status_code=400
        )

@app.route(route="login_user")
def login_user(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        email = req_body.get('email')
        password = req_body.get('password')

        engine = create_db_engine()

        user_data = {}

        with Session(engine) as session:
            user = session.scalar(select(User).where(User.email == email))

            if user is None:
                raise Exception("User with this email does not exist!")

            if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
                raise Exception("Wrong password provided!")

            user_data["id"] = user.id
            user_data["email"] = user.email
            user_data["fullname"] = user.fullname
            user_data["age"] = user.age
            user_data["description"] = user.description

        return func.HttpResponse(
            json.dumps({
                "message": "User was logged in successfully",
                "user": user_data
            }),
            status_code=202
        )
    except Exception as e:
        logging.exception(f"{str(type(e))}: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "exception": str(type(e)),
                "message": str(e)
            }),
            status_code=400
        )

@app.route(route="fetch_hobbies")
def fetch_hobbies(req: func.HttpRequest) -> func.HttpResponse:
    try:
        engine = create_db_engine()

        hobbies = []

        with Session(engine) as session:
            for hobby in session.scalars(select(Hobby)):
                hobbies.append({
                    "id": hobby.id,
                    "name": hobby.name,
                    "approved": hobby.approved,
                    "created_at": str(hobby.created_at + timedelta(hours=3))
                })

        return func.HttpResponse(
            json.dumps({
                "message": "Hobbies were fetched successfully",
                "hobbies": hobbies
            }),
            status_code=202
        )
    except Exception as e:
        logging.exception(f"{str(type(e))}: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "exception": str(type(e)),
                "message": str(e)
            }),
            status_code=400
        )

@app.route(route="fetch_channels")
def fetch_channels(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        hobby_id = req_body.get('hobby_id')

        engine = create_db_engine()

        channels = []

        with Session(engine) as session:
            for channel in session.scalars(select(Channel).where(Channel.hobby_id == hobby_id)):
                channels.append({
                    "id": channel.id,
                    "name": channel.name,
                    "hobby_id": channel.hobby_id,
                    "approved": channel.approved,
                    "created_at": str(channel.created_at + timedelta(hours=3))
                })

        return func.HttpResponse(
            json.dumps({
                "message": "Channels were fetched successfully",
                "channels": channels
            }),
            status_code=202
        )
    except Exception as e:
        logging.exception(f"{str(type(e))}: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "exception": str(type(e)),
                "message": str(e)
            }),
            status_code=400
        )

@app.route(route="fetch_messages")
def fetch_messages(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()

        channel_id = req_body.get('channel_id')

        engine = create_db_engine()

        messages = []

        with Session(engine) as session:
            for message in session.scalars(select(Message).where(Message.channel_id == channel_id)):
                user = session.scalar(select(User).where(User.id == message.user_id))
                messages.append({
                    "id": message.id,
                    "text": message.text,
                    "user_id": message.user_id,
                    "user_fullname": user.fullname,
                    "channel_id": message.channel_id,
                    "created_at": str(message.created_at + timedelta(hours=3))
                })

        return func.HttpResponse(
            json.dumps({
                "message": "Messages were fetched successfully",
                "messages": messages
            }),
            # mimetype="application/json",
            status_code=202
        )
    except Exception as e:
        logging.exception(f"{str(type(e))}: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "exception": str(type(e)),
                "message": str(e)
            }),
            status_code=400
        )