# import azure.functions as func
# import logging
from flask import Flask, jsonify, request as req
from flask_cors import CORS

import psycopg2
import bcrypt
import json
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)

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
                name TEXT NOT NULL,
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

    response_formatted = []

    for x in range(len(response)):
        element = list(response[x])
        response_formatted.append(element)
        for y in range(len(element)):
            if isinstance(element[y], datetime):
                response_formatted[x][y] = str(element[y])

    conn.close()

    return response_formatted

def get_all_channels(hobby_id):
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM channel WHERE hobby_id = %s", (hobby_id,))
    response = cur.fetchall()

    response_formatted = []

    for x in range(len(response)):
        element = list(response[x])
        response_formatted.append(element)
        for y in range(len(element)):
            if isinstance(element[y], datetime):
                response_formatted[x][y] = str(element[y])

    conn.close()

    return response_formatted

def get_all_messages(channel_id):
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM message WHERE channel_id = %s", (channel_id,))
    response = cur.fetchall()

    response_formatted = []

    for x in range(len(response)):
        element = list(response[x])
        response_formatted.append(element)
        for y in range(len(element)):
            if isinstance(element[y], datetime):
                response_formatted[x][y] = str(element[y])

    conn.close()

    return response_formatted

# app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# @app.route(route="create_user")
@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        try:
            email = req_body['email']
            password = req_body['password']
            fullname = req_body['fullname']
            age = req_body['age']
            description = req_body['description']

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
            return jsonify({
                "message": str(e),
                "status_code": 400
            })

    try:
        add_user(email, password, fullname, age, description)
        return jsonify({
            "message": "User added successfully.",
            "status_code": 200
        })
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status_code": 400
        })

# @app.route(route="create_hobby")
@app.route('/create_hobby', methods=['POST'])
def create_hobby():
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        try:
            name = req_body['name']

            if name == "":
                raise ValueError ("Not a valid name!")
        except Exception as e:
            return jsonify({
                "message": str(e),
                "status_code": 400
            })

    try:
        add_hobby(name)
        return jsonify({
            "message": "Hobby added successfully.",
            "status_code": 200
        })
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status_code": 400
        })

# @app.route(route="create_channel")
@app.route('/create_channel', methods=['POST'])
def create_channel():
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        try:
            name = req_body['name']
            hobby_id = req_body['hobby_id']

            if name == "":
                raise ValueError ("Not a valid name!")
        except Exception as e:
            return jsonify({
                "message": str(e),
                "status_code": 400
            })

    try:
        add_channel(name, hobby_id)
        return jsonify({
            "message": "Channel added successfully.",
            "status_code": 200
        })
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status_code": 400
        })

# @app.route(route="create_message")
@app.route('/create_message', methods=['POST'])
def create_message():
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        try:
            name = req_body['name']
            user_id = req_body['user_id']
            channel_id = req_body['channel_id']

            if name == "":
                raise ValueError ("Not a valid name!")
        except Exception as e:
            return jsonify({
                "message": str(e),
                "status_code": 400
            })

    try:
        add_message(name, user_id, channel_id)
        return jsonify({
            "message": "Message added successfully.",
            "status_code": 200
        })
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status_code": 400
        })

# @app.route(route="login_user")
@app.route('/login_user', methods=['POST'])
def login_user():
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        try:
            email = req_body['email']
            password = req_body['password']
        except Exception as e:
            return jsonify({
                "message": str(e),
                "status_code": 400
            })

    try:
        response = login(email, password)
        return jsonify({
            "message": "User logged in successfully.",
            "response": response,
            "status_code": 202
        })
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status_code": 400
        })

# @app.route(route="fetch_hobbies")
@app.route('/fetch_hobbies', methods=['POST'])
def fetch_hobbies():
    try:
        response = get_all_hobbies()
        return jsonify({
            "message": "Hobbies fettched successfully.",
            "response": response,
            "status_code": 202
        })
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status_code": 400
        })

# @app.route(route="fetch_channels")
@app.route('/fetch_channels', methods=['POST'])
def fetch_channels():
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        try:
            hobby_id = req_body['hobby_id']
        except Exception as e:
            return jsonify({
                "message": str(e),
                "status_code": 400
            })

    try:
        response = get_all_channels(hobby_id)
        return jsonify({
            "message": "Channels fettched successfully.",
            "response": response,
            "status_code": 202
        })
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status_code": 400
        })

# @app.route(route="fetch_messages")
@app.route('/fetch_messages', methods=['POST'])
def fetch_messages():
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        try:
            channel_id = req_body['channel_id']
        except Exception as e:
            return jsonify({
                "message": str(e),
                "status_code": 400
            })

    try:
        response = get_all_messages(channel_id)
        return jsonify({
            "message": "Messages fettched successfully.",
            "response": response,
            "status_code": 202
        })
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status_code": 400
        })

if __name__ == '__main__':
    create_tables()
    app.run() # Run the Flask app