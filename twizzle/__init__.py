import os
import psycopg2
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