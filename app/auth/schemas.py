from marshmallow import (
    fields,
    validate,
    validates_schema,
    ValidationError
)

from app.core.extensions import ma
from app.auth.models import User

class LoginSchema(ma.Schema):
    email = fields.Email(
        required=True
    )

    password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(
            min=6,
            max=255
        )
    )

class AdminCreateSchema(ma.Schema):
    email = fields.Email(
        required=True
    )

    password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(
            min=8,
            max=255
        )
    )

    confirm_password = fields.String(
        required=True,
        load_only=True
    )

    role = fields.String(
        load_default="administrator",
        validate=validate.OneOf(
            [
                "administrator",
                "super_user"
            ]
        )
    )

    @validates_schema
    def validate_passwords(
        self,
        data,
        **kargs
    ):
        if (
            data.get("password") != data.get("confirm_password")
        ):
            raise ValidationError(
                {
                    "confirm_password" :[
                        "password do not match."
                    ]
                }
            )

class UserSchema(ma.SQLAlchemyAutoSchema):

    roles = fields.Method(
        "get_role"
    )

    class Meta:

        model = User

        load_instance = False

        fields = (
            "id",
            "email",
            "is_active",
            "is_verified",
            "last_login",
            "roles",
            "created_at",
            "updated_at"
        )

    def get_role(self, obj):
        return [
            role.name for role in obj.roles
        ]
    
login_schema = LoginSchema()

admin_create_schema = AdminCreateSchema()
user_schema = UserSchema()
users_schema = UserSchema(
    many=True
)
        

