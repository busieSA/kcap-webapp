import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email 

    MAIL_SERVER = os.getenv("MAIL_SERVER")

    MAIL_PORT = os.getenv("MAIL_PORT")

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")

    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")

    MAIL_USE_SSL = os.getenv("MAIL_USER_SSL")

    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    ENQUIRY_NOTIFICATION_EMAIL = os.getenv("ENQUIRY_NOTIFICATION_EMAIL")

    # WhatsApp

    WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER")

    WHATSAPP_DEFAULT_MESSAGE = os.getenv("WHATSAPP_DEFAULT_MESSAGE")

    #website

    SITE_NAME = os.getenv("SITE_NAME")

    SITE_URL =os.getenv("SITE_URL", "http://127.0.0.1:5000")

    #Uploads 

    UPLOAD_FOLDER = BASE_DIR / "app" / "static" / "uploads"

    MAX_CONTENT_LENGHT = 10 * 1024 * 1024


class DevelopmentConfig(Config):
    DEBUG=True

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", f"sqlite:///{BASE_DIR / 'instance' / 'kcap.db'}")

class ProductionConfig(Config):

    DEBUG= True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")

class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config_by_name = {
    "development":DevelopmentConfig,
    "production":ProductionConfig,
    "testing": TestingConfig
}

 
