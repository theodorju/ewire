import smtplib
import os
from flask import url_for, request, redirect, Blueprint
from .db import get_db

bp = Blueprint('contact', __name__)


@bp.route("/", methods=["POST"])
def contact_form():
    """
    Configure route for landing page with POST method.
    Function also sends an email with the information the user has entered in
    the form
    """
    # Get the form variables, no need to validate here since validation is
    # already performed on the client side
    username = request.form.get("username")
    email = request.form.get("email")
    message = request.form.get("message")

    # Create a string with the user information
    form_info = \
        "User: {} with email: {} wrote the following:\n {}". \
            format(username, email, message)

    # Insert user to database
    db = get_db()

    # Check if the user already exists in the database
    cur = db.cursor()

    row = \
        cur.execute(
            "SELECT user_id FROM user WHERE email = ?", (email,)).fetchone()

    # If the user does not exist
    if row is None:
        # Insert user to "user" table
        cur.execute("INSERT INTO user (username, email) VALUES (?, ?)",
                    (username, email))

    # Get the user id
    user_id = cur.execute("SELECT user_id FROM user WHERE email = ?",
                          (email,)).fetchone()[0]

    # Insert message to "message" table
    cur.execute("INSERT INTO message (user_id, user_message) VALUES (?, ?)",
                (user_id, message))

    # Commit changes
    db.commit()

    # Close the database
    db.close()

    return redirect(url_for('index', _anchor="contact", submitted="submitted"))
