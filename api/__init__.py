from config import Config
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_babel import Babel

app = Flask(__name__, static_folder=Config.UPLOAD_FOLDER)
app.config.from_object(Config)
babel = Babel(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
docs = FlaskApiSpec(app)
# print(docs.__doc__)
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)


with app.app_context():
   from commands import *

@basic_auth.verify_password
def verify_password(username, password):
    from api.models.user import UserModel
    user = UserModel.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    return user


@token_auth.verify_token
def verify_token(token):
    from api.models.user import UserModel
    user = UserModel.verify_auth_token(token)
    print(f"{user=}")
    return user


@basic_auth.get_user_roles
def get_user_roles(user):
    return user.get_roles()


from flask_restful import reqparse, request
@babel.localeselector
def get_locale():
   return request.accept_languages.best_match(app.config['LANGUAGES'])


