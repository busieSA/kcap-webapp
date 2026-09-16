from app.core.base_repository import BaseRepository
from app.auth.models import User,Role

class UserRepository(BaseRepository):

    model = User

    @classmethod
    def get_by_email(cls, email):

        if not email:
            return None
        
        return (
            cls.model.query.filter(
                cls.model.email == email.strip().lower()
            ).first()
        )
    
    @classmethod
    def get_active_by_email(cls, email):

        if not email:
            return None
        
        return (
            cls.model.query.filter(
                cls.model.email == email.strip().lower(),
                cls.model.is_active.is_(True),
                cls.model.is_deleted.is_(False)
            ).first()
        )
    
    @classmethod
    def email_exists(cls, email):
        return cls.get_by_email(email) is not None
    
    @classmethod
    def get_active_users(cls):

        return (
            cls.model.query.filter(
                cls.model.is_active.is_(True),
                cls.model.delete.is_(False)
            ).order_by(
                cls.model.created_at.desc()
            ).all()
        )
    

class RoleRepository(BaseRepository):

    model = Role

    @classmethod
    def get_by_name(cls, name):
        if not name:
            return None
        
        return (
            cls.model.query.filter(
                cls.model.name == name.strip().lower()
            ).first()
        )
    
    @classmethod
    def name_exists(cls,name):
        return cls.get_by_name(name) is not None
    
    