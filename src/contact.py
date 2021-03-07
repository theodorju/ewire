import smtplib
import os
from flask import url_for, request, redirect, Blueprint

bp = Blueprint('contact', __name__)


@bp.route("/", methods=["POST"])
def contact_form():
    """
    Configure route for landing page with POST method.
    Function also sends an email with the information the user has entered in
    the form
    """
    # Get the form variables
    username = request.form.get("username")
    email = request.form.get("email")
    message = request.form.get("message")

    # Create a string with the user information
    form_info = \
        "User: {} with email: {} wrote the following:\n {}". \
            format(username, email, message)

    # Send email using Gmail
    # Configure google's smtp server listening on port 587
    server = smtplib.SMTP("smtp.gmail.com", 587)

    # Start the server
    server.starttls()

    # Get the mail and password from environmental variables
    ewire_password = os.getenv("EWIRE_PASSWORD")
    ewire_email = os.getenv("EWIRE_EMAIL")

    # Login using email and password
    server.login(ewire_email, ewire_password)

    # Send email with the users message
    server.sendmail(ewire_email, ewire_email, form_info)

    return redirect(url_for('index', _anchor="contact", submitted="submitted"))

