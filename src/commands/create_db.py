import click
from flask.cli import with_appcontext

from ..db import db


@click.command('create-db')
@with_appcontext
def create_db() -> None:
    db.drop_all()
    db.create_all()
