from flask import request

from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required
)

from marshmallow import ValidationError
from app.auth.routes import auth_bp
from app.auth.schemas import (
    login_schema,
    user_schema
)

from app.auth.service import AuthService
from app.core.responses import (
    success_response,
    error_response
)

@auth_bp.post('/login')
def login():

    if current_user.is_authenticated:
        return success_response(
            data=user_schema.dump(current_user),
            message="You are already logged in."
        )

    payload = (
        request.get_json(silent=True)
        or request.form.to_dict()
    )

    try:
        data = login_schema.load(payload)

    except ValidationError as error:
        return error_response(
            message="Please correct the login details.",
            errors=error.messages,
            status_code=422
        )

    user = AuthService.authenticate(
        email=data["email"],
        password=data["password"]
    )

    login_user(user)

    return success_response(
        data=user_schema.dump(user),
        message="Login Successful."
    )

@auth_bp.post('/logout')
@login_required
def logout():
    logout_user()
    return success_response(
        message="logout successful..."
    )

@auth_bp.get('/me')
def current_user_detials():
    return success_response(
        data=user_schema.dump(current_user)
    )


