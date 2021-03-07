import datetime
import numpy as np
from bokeh.plotting import figure
from bokeh.models import Range1d, DatetimeTicker, AdaptiveTicker
from bokeh.models.tools import HoverTool, BoxZoomTool, ResetTool, \
    LassoSelectTool, WheelZoomTool, PanTool, SaveTool
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.embed import components
from .Globals import BLUE, RED


def create_daily_load_plot(daily_forecast):
    """
    Graph the daily load forecast demand.

    Arguments:
        daily_forecast (list): list of daily forecast demand values
    """
    # Datetime range
    time_of_day = []

    # Create x-axis
    # beginning of day
    today = datetime.datetime.today()
    beginning_of_day = datetime.datetime(year=today.year, month=today.month,
                                         day=today.day)

    for i in range(len(daily_forecast)):
        time_of_day.append(beginning_of_day +
                           datetime.timedelta(minutes=i * 30))

    # Compute 75 percentile
    percentile = np.percentile(daily_forecast, 75)

    # Initialize dicts
    normal_dict = {'x': [], 'y': []}
    peak_dict = {'x': [], 'y': []}

    for i in range(len(daily_forecast)):
        if daily_forecast[i] >= percentile:
            peak_dict['x'].append(time_of_day[i])
            peak_dict['y'].append(daily_forecast[i])
        else:
            normal_dict['x'].append(time_of_day[i])
            normal_dict['y'].append(daily_forecast[i])

    # Hover tool to properly display time of day and value on hover
    hover = HoverTool(
        tooltips=[
            ("Time of day", "@x{%H:%M}"),
            ("Forecast Value", "@y MWh")
        ],
        formatters={
            '@x': 'datetime',
        },
    )

    # Create the figure
    plot = figure(x_axis_label="Time of Day",
                  y_axis_label="Megawatts Per Hour",
                  x_axis_type='datetime',
                  sizing_mode="stretch_width",
                  tools=[hover, BoxZoomTool(), ResetTool(), LassoSelectTool(),
                         WheelZoomTool(), PanTool(), SaveTool()],
                  )

    plot.xaxis.formatter = DatetimeTickFormatter(
        minutes=["%H:%M"],
        hours=["%H:%M"],

    )

    # Set x-range and y-range
    plot.y_range = Range1d(min(daily_forecast) - 500, max(daily_forecast) + 100)
    plot.x_range = Range1d(time_of_day[0] - datetime.timedelta(minutes=5),
                           time_of_day[-1] + datetime.timedelta(minutes=5))

    # Set a grid
    plot.grid.minor_grid_line_color = '#eeeeee'

    # Set the font and style of labels
    plot.axis.axis_label_text_font = "raleway"
    plot.axis.axis_label_text_font_style = "normal"

    # Set the font of ticks on the axis
    plot.axis.major_label_text_font = "raleway"

    # Set the desired ticks
    plot.xaxis.ticker = DatetimeTicker(desired_num_ticks=24)
    plot.yaxis.ticker = AdaptiveTicker(desired_num_ticks=20)

    # Add a line plot
    plot.line(time_of_day, daily_forecast,
              line_alpha=0.8,
              color=BLUE,
              line_width=1.5
              )

    # Add two circle plots one for the normal values and one for those that
    # are at or above the 75-percentile
    plot.circle('x', 'y', source=normal_dict, size=8, color=BLUE)
    plot.circle('x', 'y', source=peak_dict, size=15, color=RED)

    return components(plot)


def create_daily_res_plot(res_forecast, load_forecast):
    """
    Graph the res injection forecast.

    Arguments:
        res_forecast (list): list of renewable energy injection forecast
        load_forecast (list): list of load forecast
    """
    # Datetime range
    time_of_day = []

    # Create x-axis
    # beginning of day
    today = datetime.datetime.today()
    beginning_of_day = datetime.datetime(year=today.year, month=today.month,
                                         day=today.day)

    for i in range(len(res_forecast)):
        time_of_day.append(beginning_of_day +
                           datetime.timedelta(minutes=i * 30))

    # Compute 75 percentile
    percentile = np.percentile(res_forecast, 75)

    # Initialize dictionaries
    normal_dict = {'x': [], 'y': [], 'percentage': []}
    peak_dict = {'x': [], 'y': [], 'percentage': []}

    for i in range(len(res_forecast)):
        if res_forecast[i] >= percentile:
            peak_dict['x'].append(time_of_day[i])
            peak_dict['y'].append(res_forecast[i])
            peak_dict['percentage'].append(
                percentage_of(res_forecast[i], load_forecast[i]))
        else:
            normal_dict['x'].append(time_of_day[i])
            normal_dict['y'].append(res_forecast[i])
            normal_dict['percentage'].append(
                percentage_of(res_forecast[i], load_forecast[i]))

    # Hover tool to properly display time of day and value on hover
    hover = HoverTool(
        tooltips=[
            ("Time of day", "@x{%H:%M}"),
            ("Forecast Value", "@y MWh"),
            ("Percentage of Daily Load", "@percentage{1.11} %")
        ],
        formatters={
            '@x': 'datetime'
        },
    )

    # Create the figure
    plot = figure(x_axis_label="Time of Day",
                  y_axis_label="Megawatts Per Hour",
                  x_axis_type='datetime',
                  sizing_mode="stretch_width",
                  tools=[hover, BoxZoomTool(), ResetTool(), LassoSelectTool(),
                         WheelZoomTool(), PanTool(), SaveTool()],
                  )

    plot.xaxis.formatter = DatetimeTickFormatter(
        minutes=["%H:%M"],
        hours=["%H:%M"],

    )

    # Set x-range and y-range
    plot.y_range = Range1d(min(res_forecast) - 200, max(res_forecast) + 100)
    plot.x_range = Range1d(time_of_day[0] - datetime.timedelta(minutes=5),
                           time_of_day[-1] + datetime.timedelta(minutes=5))

    # Set a grid
    plot.grid.minor_grid_line_color = '#eeeeee'

    # Set the font and style of labels
    plot.axis.axis_label_text_font = "raleway"
    plot.axis.axis_label_text_font_style = "normal"

    # Set the font of ticks on the axis
    plot.axis.major_label_text_font = "raleway"

    # Set the desired ticks
    plot.xaxis.ticker = DatetimeTicker(desired_num_ticks=24)
    plot.yaxis.ticker = AdaptiveTicker(desired_num_ticks=20)

    # Add a line plot
    plot.line(time_of_day, res_forecast,
              line_alpha=0.2,
              color="#264b01",
              line_width=1.5
              )

    # Add two circle plots one for the normal values and one for those that
    # are at or above the 75-percentile
    plot.circle('x', 'y', source=normal_dict, size=8, color="#264b01")
    plot.circle('x', 'y', source=peak_dict, size=15, color="#264b01")

    return components(plot)


def percentage_of(a, b):
    return np.round((a / b * 100), 2)
