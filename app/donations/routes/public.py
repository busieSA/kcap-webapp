from flask import (
    request,
    current_app,
    url_for
)

from marshmallow import ValidationError

from app.donations.routes import donations_bp
from app.donations.schemas import (
    donation_create_schema,
    donation_schema
)

from app.donations.service import DonationService
from app.core.responses import (
    success_response,
    error_response
)

from app.donations.provider import get_payment_gateway


@donations_bp.post("/checkout")
def create_checkout():

    payload = (
        request.get_json(silent=True) 
        or request.form.to_dict()
    )

    try:
        data = donation_create_schema.load(
            payload
        )

    except ValidationError as error:

        return error_response(
            message=(
                "please the donation details."
            ),
            errors=error.messages,
            status_code=422
        )
    
    gateway = get_payment_gateway()

    success_url = url_for(
        "donations.donation_success",
        _external=True
    )

    cancel_url = url_for(
        "donations.donation_cancelled",
        _external=True
    )

    donation, checkout = (
        DonationService.create_and_start_checkout(
            data=data,
            gateway=gateway,
            success_url=success_url,
            cancel_url=cancel_url
        )
    )

    return success_response(
        data={
            "donation" : (
                donation_schema.dump(
                    donation
                )
            ),
            "checkout_url" : (
                checkout.checkout_url
            ),
            "provider" : (
                checkout.provider
            )
        },
        message=(
            "donation checkout created."
        )
    )

@donations_bp.get("/success")
def donation_success():

    return success_response(
        data = {
            "payment_confirmed": False
        },
        message= (
            "Thank you. Your payment is"
            "being confirmed."
        )
    )

@donations_bp.get("/cancel")
def donation_cancelled():

    return success_response(
        data={
            "payment_confirmed":False
        },
        message=(
            "The donation payment was cancelled."
        )
    )


