from app.core.base_service import BaseService
from app.core.errors import (
    ConflictError,
    UnauthorizedError,
    NotFoundError
)

from app.auth.models import User, Role
from app.auth.repository import (
    UserRepository,
    RoleRepository
)

class AuthService(BaseService):
    repository = UserRepository
    @classmethod
    def create_admin(cls,data):
        email = data["email"].strip().lower()
        password = data["password"]
        role_name = data.get(
            "role",
            "administrator"
        ).strip().lower()

        if UserRepository.email_exists(email):
            raise ConflictError(
                "A user with this email already exists."
            )
        
        role = RoleRepository.get_by_name(
            role_name
        )

        if role is None:
            raise NotFoundError(
                f"Role '{role_name}' dose not exists."
            )

        user = User(
            email=email,
            is_active=True,
            is_verified=True
        )

        user.set_password(password)

        user.add_role(role)

        UserRepository.add(user)

        return user
    
    @classmethod
    def authenticate(cls,email,password):

        email = email.strip().lower()
        user = UserRepository.get_active_by_email(email)

        if user is None:
            raise UnauthorizedError(
                "Invalid email or password."
            )
        
        if not user.check_password(password):
            raise UnauthorizedError(
                "Invalid email or password."
            )
        
        user.record_login()

        UserRepository.save()

        return user
    
    @classmethod
    def get_user(cls, user_id):
        user = UserRepository.get_by_id(
            user_id
        )

        if user is None or user.is_deleted:
            raise NotFoundError(
                "User not found."
            )

        return user

    @classmethod
    def deactivate_user(cls,user_id):
        user = cls.get_user(
            user_id
        )

        user.is_active = False

        UserRepository.save()

        return user

    @classmethod
    def activate_user(cls, user_id):
        user = cls.get_user(
            user_id
        )

        user.is_active=True
        UserRepository.save()

        return user

    @classmethod
    def assign_role(cls, user_id, role_name):
        user = cls.get_user(
            user_id
        )

        role = RoleRepository.get_by_name(
            role_name.strip().lower()
        )

        if role is None:
            raise NotFoundError(
                f"Role '{role_name}' does not exist."
            )

        user.add_role(role)

        UserRepository.save()

        return user

    @classmethod
    def remove_role(cls, user_id, role_name):
        user = cls.get_user(user_id)

        role = RoleRepository.get_by_name(
            role_name.strip().lower()
        )

        user.remove_role(role)

        UserRepository.save()

        return user

    @classmethod
    def ensure_default_roles(cls):
        default_roles = {
            "administrator":(
                "Can Access and manage the kcap admin dashboard"
            ),
            "super_user":(
                "Full admin Access."
            )
        }

        created_roles = []

        for name, description in default_roles.items():
            
            role = RoleRepository.get_by_name(
                name
            )
            
            if role is None:

                role = Role(
                    name=name,
                    description=description
                )

                RoleRepository.add(
                    role,
                    commit=False
                )

                created_roles.append(
                    role
                )

        if created_roles:
            RoleRepository.save()

        return created_roles

            

