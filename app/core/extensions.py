from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask import (
    request,
    redirect,
    url_for,
    jsonify
)


db = SQLAlchemy()

ma = Marshmallow()

migrate = Migrate()

login_manager = LoginManager()

mail = Mail()



def config_login_manager():

    login_manager.login_view = "auth.login"

    login_manager.login_message = " Please login to access this page."

    login_manager.login_message_category = "warning"

    @login_manager.unauthorized_handler
    def unauthorized():

        is_api_request = (
            request.path.startswith("/api")
            or request.path.startswith(
                "/admin/api/"
            )
        )

        if is_api_request:
            return jsonify({
                "success": False,
                "message" : (
                    "Authentication required."
                )
            }),401

        return redirect(
            url_for(
                "dashboard.login",
                next=request.url
            )
        )
    
