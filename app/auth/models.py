from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.core.extensions import db
from app.core.base_model import (
    BaseModel,
    utc_now,
    d_col
)

user_roles = db.Table(
    "user_roles",
    d_col(
        "user_id",
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    ),

    d_col(
        "role_id",
        db.Integer,
        db.ForeignKey(
            "roles.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
)

class Role(BaseModel):

    __tablename__ = "roles"

    name = d_col(
        db.String(50),
        unique=True,
        nullable=False,
        index=True
    )

    description = d_col(
        db.String(255),
        nullable=False
    )

    def __repr__(self):
        return f'<Role {self.id}>'
    

class User(UserMixin,BaseModel):

    __tablename__ = "users"

    email = d_col(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = d_col(
        db.String(255),
        nullable=False
    )

    is_active = d_col(
        db.Boolean,
        default=True,
        nullable=False
    )

    is_verified = d_col(
        db.Boolean,
        default=False,
        nullable=False
    )

    last_login = d_col(
        db.DateTime(timezone=True),
        nullable=True
    )

    roles = db.relationship(
        "Role",
        secondary=user_roles,
        lazy='selectin',
        backref=db.backref(
            "users",
            lazy="selectin"
        )

    )

    ## Password

    def set_password(self,password):
        self.password_hash = (
            generate_password_hash(
                password
            )
        )

        return self
    
    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )
    
    def record_login(self):
        self.last_login = utc_now()
        return self
    
    #Roles

    def has_role(self, role_name):
        return any(
            role.name == role_name
            for role in self.roles
        )
    
    def add_role(self, role):
        if role in self.roles:
            self.roles.append(role)
        
        return self
    
    def remove_role(self, role):
        if role in self.roles:
            self.roles.remove(role)

        return self
    

   
    
    def __repr__(self):
        return (
            f"<User "
            f"id={self.id}"
            f"email={self.email} >"
        )
    

