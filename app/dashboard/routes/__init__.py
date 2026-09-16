from flask import Blueprint


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/admin",
    template_folder="templates",
    static_folder="static",
    static_url_path="/dashboard-static"
)



from app.dashboard.routes import dashboard
from app.dashboard.routes import enquiries
from app.dashboard.routes import auth