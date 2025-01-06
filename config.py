from os import getenv


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = getenv("GOOGLE_CLIENT_SECRET")
    SECRET_KEY = getenv("SECRET_KEY")
    OAUTHLIB_INSECURE_TRANSPORT = True


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI_PROD")


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
