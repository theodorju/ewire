import datetime
import numpy as np
from bokeh.plotting import figure
from bokeh.models import Range1d, DatetimeTicker, AdaptiveTicker
from bokeh.models.tools import HoverTool, BoxZoomTool, ResetTool, \
    LassoSelectTool, WheelZoomTool, PanTool, SaveTool
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.embed import components
from Globals import BLUE, RED


def create_daily_plot(daily_forecast):
    """
    Graph the daily forecast demand.

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

    # Initialize lists that will be displayed
    y_normal = []
    x_normal = []
    y_peak = []
    x_peak = []

    for i in range(len(daily_forecast)):
        if daily_forecast[i] >= percentile:
            x_peak.append(time_of_day[i])
            y_peak.append(daily_forecast[i])
        else:
            x_normal.append(time_of_day[i])
            y_normal.append(daily_forecast[i])

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
    plot.circle(x_normal, y_normal, size=8, color=BLUE)
    plot.circle(x_peak, y_peak, size=15, color=RED)

    return components(plot)
