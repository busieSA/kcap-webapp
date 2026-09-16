# app/auth/commands.py

import click

from flask.cli import with_appcontext

from app.auth.schemas import admin_create_schema
from app.auth.service import AuthService
from app.auth.models import Role
from app.auth.repository import RoleRepository
from app.core.extensions import db


@click.command("create-admin")
@click.option(
    "--email",
    prompt=True,
    help="Administrator email address."
)
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="Administrator password."
)
@click.option(
    "--role",
    default="administrator",
    show_default=True,
    type=click.Choice(
        [
            "administrator",
            "super_admin"
        ]
    )
)
@with_appcontext
def create_admin_command(
    email,
    password,
    role
):
    """
    Create the first KCAP administrator account.
    """

    ensure_roles()

    data = admin_create_schema.load(
        {
            "email": email,
            "password": password,
            "confirm_password": password,
            "role": role
        }
    )

    user = AuthService.create_admin(
        data
    )

    click.echo(
        f"Administrator created: {user.email}"
    )


def ensure_roles():
    """
    Ensure default administrative roles exist.
    """

    roles = {
        "administrator": (
            "Can access and manage the KCAP "
            "administration dashboard."
        ),

        "super_admin": (
            "Full administrative access."
        )
    }

    for name, description in roles.items():

        existing_role = (
            RoleRepository.get_by_name(name)
        )

        if existing_role:
            continue

        role = Role(
            name=name,
            description=description
        )

        db.session.add(role)

    db.session.commit()