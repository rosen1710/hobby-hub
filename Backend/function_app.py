import azure.functions as func
import logging

import psycopg2
import bcrypt
import json
import re

def create_connection():
    conn = psycopg2.connect(
        dbname="postgres",
        user="hobby_hub",
        password="HobbHUB",
        host="my-postgresql-db.postgres.database.azure.com",
        port=5432
    )
    return conn

# Create tables if they don't exists
def create_tables():
    try:
        conn = create_connection()
        cur = conn.cursor()

        create_table = """
            CREATE TABLE IF NOT EXISTS hhuser (
                id SERIAL PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                fullname TEXT NOT NULL,
                age INT NOT NULL,
                description TEXT NOT NULL
            );
        """
        cur.execute(create_table)

        create_table = """
            CREATE TABLE IF NOT EXISTS hobby (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                approved BOOLEAN NOT NULL
            );
        """
        cur.execute(create_table)

        create_table = """
            CREATE TABLE IF NOT EXISTS hobby_user (
                id SERIAL PRIMARY KEY,
                user_id INT NOT NULL REFERENCES hhuser(id),
                hobby_id INT NOT NULL REFERENCES hobby(id)
            );
        """
        cur.execute(create_table)

        create_table = """
            CREATE TABLE IF NOT EXISTS channel (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                hobby_id INT NOT NULL REFERENCES hobby(id),
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """
        cur.execute(create_table)

        create_table = """
            CREATE TABLE IF NOT EXISTS message (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                user_id INT REFERENCES hhuser(id),
                channel_id INT NOT NULL REFERENCES channel(id),
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """
        cur.execute(create_table)

        conn.commit()
        conn.close()
    except:
        raise Exception("Error occurred while creating or accessing tables")

def add_user(email, password, fullname, age, description):
    conn = create_connection()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO hhuser (email, password_hash, fullname, age, description) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            (email, bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"), fullname, age, description))
    except psycopg2.errors.UniqueViolation:
        conn.commit()
        conn.close()
        raise psycopg2.errors.UniqueViolation("User with this email already exists!")
    except:
        conn.commit()
        conn.close()
        raise Exception("Unhandled exception occurred!")

    conn.commit()
    conn.close()

def add_hobby(name):
    conn = create_connection()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO hobby (name, approved) VALUES (%s, %s) RETURNING id;",
            (name, False))
    except psycopg2.errors.UniqueViolation:
        conn.commit()
        conn.close()
        raise psycopg2.errors.UniqueViolation("This hobby already exists!")
    except:
        conn.commit()
        conn.close()
        raise Exception("Unhandled exception occurred!")

    conn.commit()
    conn.close()

def add_channel(name, hobby_id):
    conn = create_connection()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO channel (name, hobby_id) VALUES (%s, %s) RETURNING id;",
            (name, hobby_id))
    except psycopg2.errors.UniqueViolation:
        conn.commit()
        conn.close()
        raise psycopg2.errors.UniqueViolation("This channel already exists!")
    except psycopg2.errors.ForeignKeyViolation:
        conn.commit()
        conn.close()
        raise psycopg2.errors.ForeignKeyViolation("Hobby with this id does not exists!")
    except:
        conn.commit()
        conn.close()
        raise Exception("Unhandled exception occurred!")

    conn.commit()
    conn.close()

def add_message(name, user_id, channel_id):
    conn = create_connection()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO message (text, user_id, channel_id) VALUES (%s, %s, %s) RETURNING id;",
            (name, user_id, channel_id))
    except psycopg2.errors.UniqueViolation:
        conn.commit()
        conn.close()
        raise psycopg2.errors.UniqueViolation("This message already exists!")
    except psycopg2.errors.ForeignKeyViolation:
        conn.commit()
        conn.close()
        raise psycopg2.errors.ForeignKeyViolation("User or hobby with this id does not exists!")
    except:
        conn.commit()
        conn.close()
        raise Exception("Unhandled exception occurred!")

    conn.commit()
    conn.close()

def login(email, password):
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM hhuser WHERE email = %s", (email,))

    response = cur.fetchone()

    conn.close()

    if not bcrypt.checkpw(password.encode("utf-8"), response[2].encode("utf-8")):
        raise Exception("Wrong password provided!")

    return response

def get_all_hobbies():
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM hobby")
    response = cur.fetchall()

    conn.close()

    return response

def get_all_channels(hobby_id):
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM channel WHERE hobby_id = %s", (hobby_id,))
    response = cur.fetchall()

    conn.close()

    return response

def get_all_messages(channel_id):
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM message WHERE channel_id = %s", (channel_id,))
    response = cur.fetchall()

    conn.close()

    return response

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="create_user")
def create_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger called create_user function')

    try:
        # create_tables()
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        try:
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
        except Exception as e:
            return func.HttpResponse(
                str(e),
                status_code=400
            )

    try:
        add_user(email, password, fullname, age, description)
        return func.HttpResponse(
            "User added successfully.",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=400
        )

@app.route(route="create_hobby")
def create_hobby(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger called create_hobby function')

    try:
        # create_tables()
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        try:
            name = req_body.get('name')

            if name == "":
                raise ValueError ("Not a valid name!")
        except Exception as e:
            return func.HttpResponse(
                str(e),
                status_code=400
            )

    try:
        add_hobby(name)
        return func.HttpResponse(
            "Hobby added successfully.",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=400
        )

@app.route(route="create_channel")
def create_channel(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger called create_channel function')

    try:
        # create_tables()
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        try:
            name = req_body.get('name')
            hobby_id = req_body.get('hobby_id')

            if name == "":
                raise ValueError ("Not a valid name!")
        except Exception as e:
            return func.HttpResponse(
                str(e),
                status_code=400
            )

    try:
        add_channel(name, hobby_id)
        return func.HttpResponse(
            "Channel added successfully.",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=400
        )

@app.route(route="create_message")
def create_message(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger called create_message function')

    try:
        # create_tables()
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        try:
            name = req_body.get('name')
            user_id = req_body.get('user_id')
            channel_id = req_body.get('channel_id')

            if name == "":
                raise ValueError ("Not a valid name!")
        except Exception as e:
            return func.HttpResponse(
                str(e),
                status_code=400
            )

    try:
        add_message(name, user_id, channel_id)
        return func.HttpResponse(
            "Message added successfully.",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=400
        )

@app.route(route="login_user")
def login_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger called login_user function')

    try:
        # create_tables()
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        try:
            email = req_body.get('email')
            password = req_body.get('password')
        except Exception as e:
            return func.HttpResponse(
                str(e),
                status_code=400
            )

    try:
        response = login(email, password)
        return func.HttpResponse(
            json.dumps({
                "message": "User logged in successfully.",
                "response": response
            }),
            status_code=202
        )
    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=400
        )

@app.route(route="get_all_hobbies")
def get_all_hobbies(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger called get_all_hobbies function')

    try:
        response = get_all_hobbies()
        return func.HttpResponse(
            json.dumps({
                "message": "Hobbies fettched successfully.",
                "response": response
            }),
            status_code=202
        )
    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=400
        )

@app.route(route="get_all_channels")
def get_all_channels(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger called get_all_channels function')

    try:
        # create_tables()
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        try:
            hobby_id = req_body.get('hobby_id')
        except Exception as e:
            return func.HttpResponse(
                str(e),
                status_code=400
            )

    try:
        response = get_all_channels(hobby_id)
        return func.HttpResponse(
            json.dumps({
                "message": "Channels fettched successfully.",
                "response": response
            }),
            status_code=202
        )
    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=400
        )

@app.route(route="get_all_messages")
def get_all_messages(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger called get_all_messages function')

    try:
        # create_tables()
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        try:
            channel_id = req_body.get('channel_id')
        except Exception as e:
            return func.HttpResponse(
                str(e),
                status_code=400
            )

    try:
        response = get_all_messages(channel_id)
        return func.HttpResponse(
            json.dumps({
                "message": "Messages fettched successfully.",
                "response": response
            }),
            status_code=202
        )
    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=400
        )