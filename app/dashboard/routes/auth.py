
from flask import (
    render_template,
    redirect,
    url_for
)
from flask_login import current_user
from app.dashboard.routes import dashboard_bp

@dashboard_bp.get('/login')
def login():

    """
        Admin login Page here...
    """

    if current_user.is_authenticated:
        return redirect(
            url_for("dashboard.index")
        )
    
    return render_template(
        "dashboard/auth/login.html"
    )

