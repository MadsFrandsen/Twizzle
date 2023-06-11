import os
import psycopg2
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, current_app
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from psycopg2.extras import RealDictCursor
from flask_mail import Mail
from twizzle.config import Config

env_path = Path('../.env')
load_dotenv(dotenv_path=env_path)


bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

current_dir = os.getcwd()

data_base = os.path.join(current_dir, 'twizzle/init_database.sql')
db_file = open(data_base)

hased_csv_path = os.path.join(current_dir, 'twizzle/dataset/only_hashed.csv')
post_data_csv_path = os.path.join(current_dir, 'twizzle/dataset/post_data.csv')
follow_data_csv_path = os.path.join(current_dir, 'twizzle/dataset/follows.csv')


conn = psycopg2.connect(
    host="localhost",
    port="5123",
    dbname=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASS')
)
cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute(db_file.read())
db_file.close()

cur.execute(f"""
    COPY Users(email_address, user_name, password)
    FROM '{hased_csv_path}'
    DELIMITER ','
    CSV HEADER;
""")

cur.execute(f"""
    COPY Posts(title, content, user_id)
    FROM '{post_data_csv_path}'
    DELIMITER ','
    CSV HEADER;
""")

cur.execute(f"""
    COPY Follows(user_id1, user_id2)
    FROM '{follow_data_csv_path}'
    DELIMITER ','
    CSV HEADER;
""")

conn.commit()


def init_users(data):
    from twizzle.queries import init_user

    for _, row in data.iterrows():
        email_address = row['email_address']
        user_name = row['user_name']
        password = row['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        init_user(email_address, user_name, hashed_password)


def create_app(config_cass=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from twizzle.users.routes import users
    from twizzle.posts.routes import posts
    from twizzle.main.routes import main
    from twizzle.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)


    return app



# cur.close()
# conn.close()