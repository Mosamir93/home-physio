from os import getenv


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = getenv("GOOGLE_CLIENT_SECRET")


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI_PROD")


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
