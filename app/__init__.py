import os

from pathlib import Path

from dotenv import load_dotenv
load_dotenv()


from flask import Flask

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


def create_app(config_name=None):


    app = Flask(__name__)

    Path(
        app.instance_path
    ).mkdir(
            parents=True,
            exist_ok=True
        )

    config_name = (
        config_name or os.getenv("FLASK_ENV") or "development"
    )

    config_class = config_by_name.get(
        config_name,
        config_by_name["development"]
    )

    app.config.from_object(config_class)

    # Extensions
    db.init_app(app)
    ma.init_app(app)

    register_models()

    migrate.init_app(app)
    login_manager.init_app(app)

    import app.auth as auth_package

    mail.init_app(app)

    config_login_manager()

    # Error handlers
    register_error_handlers(app)

    # Blueprints
    register_blueprints(app)


    register_commands(app)
    return app


def register_blueprints(app):
    from app.website import website_bp
    from app.contact.routes import contact_bp
    from app.auth.routes import auth_bp
    from app.dashboard.routes import dashboard_bp
    from app.donations.routes import donations_bp

    app.register_blueprint(website_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(donations_bp)

    
def register_models():

    from app.contact.models import Enquiry

    from app.auth.models import (
        User,
        Role,
        user_roles
    )

    from app.donations.models import Donation

def register_commands(app):

    from app.auth.commands import (
        create_admin_command
    )

    app.cli.add_command(
        create_admin_command
    )