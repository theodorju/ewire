import smtplib
import os
from flask import Flask, render_template, url_for, request, redirect
from Dashboard import create_daily_plot


# Create flask instance
app = Flask(__name__, static_folder='static')

# Set SEND_FILE_MAX_AGE_DEFAULT for development purposes to enforce CSS to be
# reloaded at refresh
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/", methods=["GET"])
def index():
    """
    Configure route for landing page with GET method
    """
    return render_template("index.html")


@app.route("/", methods=["POST"])
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


@app.route("/daily")
def daily():
    # Hardcoded-values for testing
    values = [4910.0, 4820.0, 4820.0, 4780.0, 4660.0, 4550.0, 4460.0, 4460.0,
              4450.0, 4470.0, 4540.0, 4610.0, 4700.0, 4860.0, 5060.0, 5300.0,
              5590.0, 5850.0, 6090.0, 6290.0, 6440.0, 6540.0, 6600.0, 6600.0,
              6550.0, 6360.0, 6060.0, 5960.0, 6000.0, 5970.0, 5880.0, 5760.0,
              5620.0, 5760.0, 6190.0, 6550.0, 6830.0, 6840.0, 6840.0, 6760.0,
              6590.0, 6400.0, 6180.0, 5970.0, 5770.0, 5600.0, 5440.0, 5110.0]

    script, plot = create_daily_plot(values)

    return render_template("daily.html", script=script, plot=plot)


@app.route("/renewable")
def renewable():
    return render_template("renewable.html")


@app.route("/consumer")
def consumer():
    return render_template("consumer.html")
