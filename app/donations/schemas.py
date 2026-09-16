from marshmallow import (
    fields,
    validate,
    validates,
    ValidationError
)

from app.core.extensions import ma
from app.donations.models import Donation


class DonationCreateSchema(ma.Schema):

    donor_name = fields.String(
        allow_none=True,
        load_default=None,
        validate=validate.Length(max=150)
    )

    donor_email = fields.Email(
        required=True,
        allow_none=False
    )

    donor_phone = fields.String(
        allow_none=True,
        load_default=None,
        validate=validate.Length(max=50)
    )

    amount = fields.Decimal(
        required=True,
        as_string=False,
        places=2
    )

    currency = fields.String(
        load_default="ZAR",
        validate=validate.OneOf([
            "ZAR",
            "USD",
            "GBP",
            "EUR"
        ])
    )

    purpose = fields.String(
        allow_none=True,
        load_default=None,
        validate=validate.Length(max=255)
    )

    message = fields.String(
        allow_none=True,
        load_default=None
    )

    is_anonymous = fields.Boolean(
        load_default=False
    )


    @validates("amount")
    def validate_amount(self, value, **kwargs):

        if value <= 0:
            raise ValidationError(
                "Donation amount must be greater than zero."
            )


class DonationSchema(ma.SQLAlchemyAutoSchema):

    class Meta:

        model = Donation

        load_instance = True

        fields = (
            "id",
            "reference",

            "donor_name",
            "donor_email",
            "donor_phone",

            "amount",
            "currency",

            "purpose",
            "message",
            "is_anonymous",

            "provider",
            "provider_reference",
            "provider_session_reference",

            "status",

            "paid_at",
            "failed_at",
            "cancelled_at",
            "refunded_at",

            "created_at",
            "updated_at"
        )


donation_create_schema = DonationCreateSchema()

donation_schema = DonationSchema()

donations_schema = DonationSchema(
    many=True
)