from flask import (
    render_template,
    request
)

from flask_login import login_required
from app.dashboard.routes import dashboard_bp

from app.contact.repository import EnquiryRepository
from app.contact.service import EnquiryService
from app.contact.schemas import (
    enquiry_schema,
    enquiries_schema
)

from app.core.responses import success_response
from app.auth.decorators import role_required


@dashboard_bp.get("/enquiries")
@role_required(
    "administrator",
    "super_admin"
)
def enquiries():

    status = request.args.get(
        "status",
        ""
    ).strip().lower()

    keyword = request.args.get(
        "q",
        ""
    ).strip()

    if keyword:
        query = (
            EnquiryRepository.search_enquiries(keyword)
        )

        enquirires_list = (
            query.order_by(
                EnquiryRepository.model.created_at.desc()
            ).all()
        )

    elif status == "new":
        enquiry_list = (
            EnquiryRepository.get_new()
        )

    elif status == "read":
        enquiry_list = (
            EnquiryRepository.get_read()
        )

    elif status == "resolved":
        enquiry_list = (
            EnquiryRepository.get_resolved()
        )

    else:
        enquiry_list = (
            EnquiryRepository.get_all_ordered()
        )

    return render_template(
        "dashboard/enquiries/index.html",
        enquiries=enquiry_list,
        selected_status=status,
        keyword=keyword,
        new_enquiries = (
            EnquiryRepository.count_new()
        )
    )

@dashboard_bp.get("/enquiries/<int:enquiry_id>")
@role_required(
    "administrator",
    "super_admin"
)
def enquiry_details(enquiry_id):

    """
        View single enquiry
    """ 

    enquiry = (
        EnquiryService.get_enquiry(
            enquiry_id
        )
    )

    if enquiry.is_new:
        enquiry = (
            EnquiryService.mark_as_read(
                enquiry_id
            )
        )

    return render_template(
        "dashboard/enquiries/view.html",
        new_enquiries = (
            EnquiryRepository.count_new()
        )
    )

@dashboard_bp.post("/api/enquiries/<int:enquiry_id>/read")
@role_required(
    "administrator",
    "super_admin"
)
def mark_enquiry_read(enquiry_id):

    enquiry = (
        EnquiryService.mark_as_read(
            enquiry_id
        )
    )

    return success_response(
        data=enquiry_schema.dump(enquiry),
        message="Enquiry Marked as read."
    )

@dashboard_bp.post("/api/enquiries/<int:enquiry_id>/resolve")
@role_required(
    "administrator",
    "super_admin"
)
def resolve_enquiry(enquiry_id):

    enquiry = (
        EnquiryService.resolve(
            enquiry_id
        )
    )

    return success_response(
        data=enquiry_schema.dump(enquiry),
        message="Enquiry resolved."
    )

@dashboard_bp.post("/api/enquiries/<int:enquiry_id>/reopen")
@role_required(
    "administrator",
    "super_admin"
)
def reopen_enquiry(enquiry_id):
    enquiry = (
        EnquiryService.reopen(
            enquiry_id
        )
    )

    return success_response(
        data=enquiry_schema.dump(enquiry),
        message="Enquiry reopened."
    )

@dashboard_bp.post("/api/enquiries/<int:enquiry_id>/archive")
@role_required(
    "administrator",
    "super_admin"
)
def archive_enquiry(enquiry_id):
    enquiry = (
        EnquiryService.archive(
            enquiry_id
        )
    )

    return success_response(
        data={
            "id": enquiry.id
        },
        message="Enquiry archived."
    )


