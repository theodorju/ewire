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


if __name__ == "__main__":
    # Placeholder data
    load_values = [4160.0, 4030.0, 3990.0, 3940.0, 3860.0, 3800.0, 3750.0,
                   3710.0, 3660.0, 3660.0, 3810.0, 3900.0, 3980.0, 4130.0,
                   4370.0, 4590.0, 4810.0, 5050.0, 5300.0, 5480.0, 5600.0,
                   5720.0, 5830.0, 5820.0, 5670.0, 5390.0, 5320.0, 5310.0,
                   5250.0, 5150.0, 5090.0, 5080.0, 5260.0, 5630.0, 5960.0,
                   6230.0, 6240.0, 6190.0, 6090.0, 5940.0, 5720.0, 5440.0,
                   5240.0, 5140.0, 4980.0, 4780.0, 4520.0]

    res_values = [1330.0, 1380.0, 1440.0, 1500.0, 1560.0, 1620.0, 1680.0,
                  1740.0, 1780.0, 1810.0, 1830.0, 1830.0, 1860.0, 1910.0,
                  2000.0, 2090.0, 2180.0, 2240.0, 2280.0, 2300.0, 2290.0,
                  2260.0, 2220.0, 2150.0, 2100.0, 2010.0, 1910.0, 1810.0,
                  1710.0, 1590.0, 1450.0, 1300.0, 1120.0, 970.0, 850.0,
                  790.0, 760.0, 740.0, 710.0, 680.0, 660.0, 630.0, 610.0,
                  580.0, 560.0, 550.0, 530.0, 520.0]

    script, div = create_daily_load_plot(load_values)
    print("Script: {}\n\n".format(script))
    print("Div: {}".format(div))
