from typing import Dict
from flask_login import UserMixin
from psycopg2 import sql
from twizzle import cur, login_manager
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
import twizzle.queries


@login_manager.user_loader
def load_user(user_id):
    user_sql = sql.SQL("""
        SELECT *
        FROM Users
        WHERE user_id = %s
        """).format(sql.Identifier('id'))
    cur.execute(user_sql, (int(user_id),))
    return User(cur.fetchone()) if cur.rowcount > 0 else None


class ModelUserMixin(dict, UserMixin):
    @property
    def _id(self):
        return self.id

class ModelMixin(dict):
    pass


class User(ModelUserMixin):
    def __init__(self, user_data: Dict):
        super(User, self).__init__(user_data)
        self.id = user_data.get('user_id')
        self.email_address = user_data.get('email_address')
        self.user_name = user_data.get('user_name')
        self.password = user_data.get('password')
        self.image_file = user_data.get('image_file')
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return twizzle.queries.get_user_by_id(user_id)


class Post(ModelUserMixin):
    def __init__(self, post_data: Dict):
        super(Post, self).__init__(post_data)
        self.pid = post_data.get('pid')
        self.uid = post_data.get('uid')
        self.title = post_data.get('title')
        self.content = post_data.get('content')




