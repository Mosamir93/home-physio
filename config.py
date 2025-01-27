from os import getenv
from dotenv import load_dotenv


load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = getenv("GOOGLE_CLIENT_SECRET")
    SECRET_KEY = getenv("SECRET_KEY")
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
    WTF_CSRF_ENABLED = False
    JWT_TOKEN_LOCATION = 'cookies'
    OAUTHLIB_INSECURE_TRANSPORT = True
    REDIS_URL = "redis://localhost:6379/0"


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI_PROD")


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
