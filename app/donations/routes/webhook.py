from flask import request, current_app

from app.donations.routes import donations_bp

from app.donations.service import DonationService

from app.donations.gateway import (
    WebhookVerificationError
)

from app.donations.schemas import (
    donation_schema
)

from app.core.responses import (
    success_response,
    error_response
)

from app.donations.provider import get_payment_gateway


@donations_bp.post('/webhook')
def payment_webhook():
    """
    Receive payment-provider webhook events.
    """

    gateway = get_payment_gateway()

    payload = request.get_data()

    headers = dict(
        request.headers
    )

    try:

        donation = (
            DonationService.process_webhook(
                gateway=gateway,
                payload=payload,
                headers=headers
            )
        )
    except WebhookVerificationError:

        return error_response(
            message= (
                "Webhook verification failed."
            ),
            status_code=400
        )

    return success_response(
        data=donation_schema.dump(
            donation
        ),
        message=(
            "webhook processed successfully."
        )
    )

