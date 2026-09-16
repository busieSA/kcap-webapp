from flask import Blueprint

website_bp = Blueprint(
    'website',
    __name__,
    url_prefix='/',
    template_folder="templates",
    static_folder="static",
    static_url_path="/website-static"
)

from app.website.routes import donate

