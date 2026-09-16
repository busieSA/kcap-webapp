from flask import render_template
from flask_login import login_required,current_user
from app.dashboard.routes import dashboard_bp
from app.contact.repository import EnquiryRepository

from app.auth.decorators import role_required

@dashboard_bp.get("/")
@role_required(
    "administrator",
    "super_admin"
)
def index():
    total_enquiries = (
        EnquiryRepository.count()
    )

    new_enquiries = (
        EnquiryRepository.count_new()
    )

    resolved_enquiries = (
        EnquiryRepository.count_resolved()
    )

    recent_enquiries = (
        EnquiryRepository.get_all_ordered()[:5]
    )

    return render_template(
        "dashboard/index.html",
        current_user=current_user,
        total_enquiries=total_enquiries,
        new_enquiries=new_enquiries,
        resolved_enquiries=resolved_enquiries,
        recent_enquiries=recent_enquiries
    )


