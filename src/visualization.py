import json
from datetime import date
from flask import render_template, Blueprint
from .Dashboard import create_daily_load_plot, create_daily_res_plot

bp = Blueprint('visualizations', __name__)


@bp.route("/daily")
def daily():
    # Open json file

    with open('ewire/data/daily_forecast.json') as json_file:
        loaded_json = json.load(json_file)

    # Extract target values from json file
    target_date = date.today().strftime("%Y%m%d")
    values = loaded_json[target_date]

    # Create the plot
    script, plot = create_daily_load_plot(values)

    # Render template
    return render_template("daily.html", script=script, plot=plot)


@bp.route("/renewable")
def renewable():
    # Open json file
    with open('ewire/data/res_forecast.json') as json_file:
        res_json = json.load(json_file)

    # Extract target values from json file
    target_date = date.today().strftime("%Y%m%d")
    res_values = res_json[target_date]

    # Extract load forecast to calculate percentages
    with open('ewire/data/daily_forecast.json') as json_file:
        forecast_json = json.load(json_file)
    forecast_values = forecast_json[target_date]

    # Create the plot
    script, plot = create_daily_res_plot(res_values, forecast_values)

    # Render template
    return render_template("renewable.html", script=script, plot=plot)


@bp.route("/consumer")
def consumer():
    return render_template("consumer.html")
