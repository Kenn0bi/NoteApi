from pathlib import Path
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

BASE_DIR = Path(__file__).parent


class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'main.db'}"
    TEST_DATABASE = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Зачем эта настройка: https://flask-sqlalchemy-russian.readthedocs.io/ru/latest/config.html#id2
    DEBUG = True
    PORT = 5000
    SECRET_KEY = "My secret key =)"
    RESTFUL_JSON = {
        'ensure_ascii': False,
    }
    APISPEC_SPEC = APISpec(
            title='Notes Project',
            version='v1',
            plugins=[MarshmallowPlugin()],
            securityDefinitions={
                "basicAuth": {
                    "type": "basic"
                }
            },
            security=[],

            openapi_version='2.0.0'
    )
    APISPEC_SWAGGER_URL = '/swagger'
    APISPEC_SWAGGER_UI_URL = '/swagger-ui'
    LANGUAGES = ['en', 'ru']