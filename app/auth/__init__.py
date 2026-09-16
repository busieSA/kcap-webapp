from app.core.extensions import (
    login_manager,
    db
)

@login_manager.user_loader
def load_user(user_id):

    from app.auth.models import User

    try:
        user_id = int(user_id)

    except (TypeError, ValueError):
        return None
    
    return db.session.get(
        User,
        user_id
    )

