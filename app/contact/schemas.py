from marshmallow import (
    fields,
    validate
)

from app.core.extensions import ma
from app.contact.models import Enquiry

class EnquiryCreateSchema(ma.Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(
            min=2,
            max=255
        )
    )

    email = fields.Email(
        required=True
    )

    phone = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(
            max=30
        )
    )

    subject = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(
            max=255
        )
    )

    message = fields.String(
        required=True,
        validate=validate.Length(
            min=6,
            max=5000
        )
    )

class EnquirySchema(ma.SQLAlchemyAutoSchema):
    status = fields.Method("get_status")

    def get_status(self, obj):
        return obj.status.value if obj.status else None
    class Meta:
        model = Enquiry

        load_instance = True

        include_fk = True

        fields = (
            "id",
            "name",
            "email",
            "phone",
            "subject",
            "message",
            "status",
            "is_registered",
            "read_at",
            "resolved_at",
            "created_at",
            "updated_at"
        )

enquiry_create_schema = EnquiryCreateSchema()
enquiry_schema = EnquirySchema()
enquiries_schema = EnquirySchema(
    many=True
)

