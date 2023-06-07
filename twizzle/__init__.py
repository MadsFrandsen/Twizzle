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


data_base = os.path.join(os.getcwd(), 'twizzle/init_database.sql')
db_file = open(data_base)


conn = psycopg2.connect(
    host="localhost",
    dbname="FlaskBlog",
    user="postgres",
    password="",
    port="5123"
)
cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute(db_file.read())
conn.commit()


def init_users(data):
    from twizzle.queries import init_user

    # data = {'email_address': ['test@gmail.com'],
    #     'user_name': ['test'],
    #     'password': ['123']}
    
    # df = pandas.DataFrame(data)

    # hashed_password = bcrypt.generate_password_hash(df['password']).decode('utf-8')
    # user_data = dict(email_address='test@gmail.com',
    #                      user_name='test',
    #                      password=hashed_password)

    for _, row in data.iterrows():
        email_address = row['email_address']
        user_name = row['user_name']
        password = row['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        init_user(email_address, user_name, hashed_password)



    # hashed_password = bcrypt.generate_password_hash('123').decode('utf-8')
    # user_data = dict(email_address='test@gmail.com',
    #                      user_name='test',
    #                      password=hashed_password)
    # init_user(user_data)


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

    # data = pd.read_csv('/Users/madsfrandsen/Documents/DIS/Group_Project/twizzle/dataset/MOCK_DATA.csv')
    # init_users(data)

    return app



# cur.close()
# conn.close()