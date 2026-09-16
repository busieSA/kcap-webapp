# app/core/config.py

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTANCE_DIR = BASE_DIR / "instance"
DATABASE_FILE = INSTANCE_DIR / "kcap.db"


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-change-this"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    MAIL_USE_TLS = (
        os.getenv("MAIL_USE_TLS", "true").lower()
        == "true"
    )

    MAIL_USE_SSL = (
        os.getenv("MAIL_USE_SSL", "false").lower()
        == "true"
    )

    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER",
        MAIL_USERNAME
    )

    ENQUIRY_NOTIFICATION_EMAIL = os.getenv(
        "ENQUIRY_NOTIFICATION_EMAIL"
    )

    # WhatsApp
    WHATSAPP_NUMBER = os.getenv(
        "WHATSAPP_NUMBER"
    )

    WHATSAPP_DEFAULT_MESSAGE = os.getenv(
        "WHATSAPP_DEFAULT_MESSAGE",
        "Hello KCAP, I would like more information."
    )

    # Website
    SITE_NAME = os.getenv(
        "SITE_NAME",
        "KCAP"
    )

    SITE_URL = os.getenv(
        "SITE_URL",
        "http://127.0.0.1:5000"
    )


class DevelopmentConfig(Config):

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{DATABASE_FILE}"
    )


class ProductionConfig(Config):

    DEBUG = False

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL"
    )


class TestingConfig(Config):

    TESTING = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}