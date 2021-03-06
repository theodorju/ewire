import smtplib
import os
import json
from datetime import date
from flask import Flask, render_template, url_for, request, redirect
from apscheduler.schedulers.background import BackgroundScheduler
from Dashboard import create_daily_plot
from Scrapper import download_daily_forecast


def prepare_file():
    """ Function for test purposes. """

    # Update daily forecast json file
    download_daily_forecast()


# Background scheduler to download and parse file
job = BackgroundScheduler()

# Scheduler will run daily at 4 AM
job.add_job(prepare_file, 'cron', hour=4)
job.start()

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
    # Open json file
    with open('data/daily_forecast.json') as json_file:
        loaded_json = json.load(json_file)

    # Extract target values from json file
    target_date = date.today().strftime("%Y%m%d")
    values = loaded_json[target_date]

    # Create the plot
    script, plot = create_daily_plot(values)

    # Render template
    return render_template("daily.html", script=script, plot=plot)


@app.route("/renewable")
def renewable():
    return render_template("renewable.html")


@app.route("/consumer")
def consumer():
    return render_template("consumer.html")
