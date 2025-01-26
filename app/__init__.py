from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from os import getenv
import os


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name="development"):
    app = Flask(__name__, template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'))

    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    from .routes.general import general_bp
    from .routes.patient import patient_bp
    from .routes.physiotherapists import physio_bp
    from .auth.routes import auth_bp


    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(patient_bp, url_prefix='/patient')
    app.register_blueprint(physio_bp, url_prefix='/physio')
    app.register_blueprint(general_bp)
    return app
