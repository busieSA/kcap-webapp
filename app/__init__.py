import os

from flask import Flask
from dotenv import load_dotenv

from app.core.config import config_by_name
from app.core.extensions import (
    db,
    ma,
    migrate,
    login_manager,
    mail,
    config_login_manager
)

from app.core.error_handlers import register_error_handlers

def create_app():

    load_dotenv()

    app = Flask(__name__)

    config_name = (
        config_name or os.getenv("FLASK_ENV") or "development"
    )

    config_class = config_by_name.get(
        config_name,
        config_by_name["development"]
    )

    app.config.from_object(config_class)

    #ext

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    config_login_manager()

    #Eror

    register_error_handlers(app)

    #blueprints

    return app

