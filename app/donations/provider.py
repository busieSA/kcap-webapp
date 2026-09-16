from flask import current_app

def get_payment_gateway():

    gateway = current_app.extensions.get(
        "payment_gateway"
    )

    if gateway is None:

        raise RuntimeError(
            "No payment gateway has been configured."
        )
    
    return gateway


