from marshmallow import ValidationError
from flask import request
from app.contact.routes import contact_bp

from app.contact.schemas import (
    enquiry_create_schema,
    enquiry_schema
)

from app.contact.service import EnquiryService

from app.core.responses import (
    success_response,
    error_response
)

@contact_bp.post("/enquiries")
def submit_enquiry():
    
    payload = request.get_json(
        silent=True
    ) or request.form.to_dict()

    try:
        data = enquiry_create_schema.load(
            payload
        )

    except ValidationError as error:
        return error_response(
            message="Please correct the highlighted fields.",
            errors=error.messages,
            status_code=422
        )
    
    enquiry, email_sent = (
        EnquiryService.submit_enquiry(data)
    )

    response_data = enquiry_schema.dump(enquiry)

    response_data["notification_email_sent"] = (
        email_sent
    )

    return success_response(
        data=response_data,
        message="Your enquiry has been submitted successfully.",
        status_code=201
    )


