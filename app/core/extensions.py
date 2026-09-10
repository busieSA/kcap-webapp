from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail



db = SQLAlchemy()

ma = Marshmallow()

migrate = Migrate()

login_manager = LoginManager()

mail = Mail()



def config_login_manager():

    login_manager.login_view = "auth.login"

    login_manager.login_message = " Please login to access this page."

    login_manager.login_message_category = "warning"

    
