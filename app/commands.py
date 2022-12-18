from app.extensions import db
from app.views.auth.models import User, Role

from flask.cli import with_appcontext
import click


@click.command("init_db")
@with_appcontext
def init_db():
    click.echo("Initializing db")
    db.drop_all()
    db.create_all()
    click.echo("Created db")


@click.command("populate_db")
@with_appcontext
def populate_db():

    user_role = Role(name="user")
    admin_role = Role(name="admin")
    db.session.add_all([user_role, admin_role])
    db.session.flush()

    admin = User(first_name="Admin", last_name="Admin", email="admin@mail.com", password="password123")
    admin.roles.append(admin_role)
    db.session.add(admin)
    db.session.commit()