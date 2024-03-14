import azure.functions as func
import logging

import psycopg2
import bcrypt

def create_connection():
    conn = psycopg2.connect(
        dbname="postgres",
        user="hobby_hub",
        password="HobbHUB",
        host="my-postgresql-db.postgres.database.azure.com",
        port=5432
    )
    return conn

# Create tables if they don't exist
def create_tables():
    try:
        conn = create_connection()
        cur = conn.cursor()

        user_table = """
            CREATE TABLE IF NOT EXISTS hhuser (
                id SERIAL PRIMARY KEY,
                email TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                fullname TEXT NOT NULL,
                age INTEGER NOT NULL,
                description TEXT NOT NULL
            );
        """

        hobby_table = """
            CREATE TABLE IF NOT EXISTS hobby (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                approved BOOLEAN NOT NULL
            );
        """

        cur.execute(user_table)
        cur.execute(hobby_table)

        conn.commit()
        conn.close()
        print('Tables created or already exist')
    except:
        print('Error occurred while creating or accessing tables')
        exit()

def add_user(email, password, fullname, age, description):
    conn = create_connection()
    cur = conn.cursor()

    # password = 

    cur.execute("INSERT INTO hhuser (email, password_hash, fullname, age, description) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                (email, bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()), fullname, age, description))
    user_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return func.HttpResponse(
             "User added successfully",
             status_code=200
        )

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="create_user")
def create_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # try:
    #     create_tables()
    #     req_body = req.get_json()
    # except ValueError:
    #     pass
    # else:
    #     try:
    #         email = req_body.get('email')
    #         password = req_body.get('password')
    #         fullname = req_body.get('fullname')
    #         age = req_body.get('age')
    #         description = req_body.get('description')
    #     except:
    #         return func.HttpResponse(
    #          "Not valid data provided!",
    #          status_code=400
    #     )

    if True: # email and password and fullname and age and description:
        # add_user(email, password, fullname, age, description)
        add_user("email", "password", "fullname", 17, "description")
        return func.HttpResponse(
            "User added successfully.",
            status_code=200
        )
    else:
        return func.HttpResponse(
             "Not valid data provided!",
             status_code=400
        )