from functools import wraps
from flask_login import (
    current_user,
    login_required
)

from app.core.errors import ForbiddenError


def role_required(*roles):

    """
    
        Restrict a route to user with atleast on of the supplied roles
    
        
        Example :

            @role_required("administrator", "super_user")
            def dashboard():
                ...
    """

    def decorator(view_function):
        @wraps(view_function)
        @login_required
        def wrapped_view(*args, **kwargs):

            allowed = any(
                current_user.has_role(role) for role in roles
            )

            if not allowed:
                raise ForbiddenError(
                    "You do not have permission to access this resource"
                )
            
            return view_function(
                *args,
                **kwargs
            )
        
        return wrapped_view
    return decorator

