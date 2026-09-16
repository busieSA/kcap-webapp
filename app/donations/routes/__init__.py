from flask import Blueprint

donations_bp = Blueprint(
    "donations",
    __name__,
    url_prefix="/api/donations"
)

from app.donations.routes import public
from app.donations.routes import webhook

