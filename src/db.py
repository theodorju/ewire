import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
    Connect to the database
    """
    # Establish db connection to the file pointed by current_app DATABASE
    # configuration
    db = sqlite3.connect(
        current_app.config['DATABASE'],
        detect_types=sqlite3.PARSE_DECLTYPES
    )

    # Return rows that behave like dictionaries
    db.row_factory = sqlite3.Row

    # Return the connection
    return db


def init_db():
    """
    Initialize the database based on schema.sql
    """
    db = get_db()

    # Open schema.sql file relative to the ewire package
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')  # Define a command line command called init-db
@with_appcontext
def init_db_command():
    """Clear any existing data and create new tables."""
    init_db()
    click.echo("Initialized database.")


def init_app(app):
    """
    Register close_db and init_db_command to the application.
    Arguments:
        app (Flask obj): Flask application
    """

    # Add new command
    app.cli.add_command(init_db_command)
