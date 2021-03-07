import json
import urllib.request
import re
import openpyxl as op
from bs4 import BeautifulSoup
from datetime import date, timedelta
from .Globals import ADMIE_SITE_PREFIX, ADMIE_LOAD_FORECAST_URL, \
    LATEST_LOAD_FORECAST_SELECTOR, EARLIEST_LOAD_FORECAST_SELECTOR, \
    COLUMN_START, COLUMN_END, LATEST_RES_FORECAST_SELECTOR, \
    EARLIEST_RES_FORECAST_SELECTOR


def download_daily_forecast():
    """
    Download the daily load forecast excel file from ADMIE.
    Tries to download the latest file that is indicated by "ISP2". If that
    download fails, it downloads the earliest file instead (indicated by "ISP1")
    """

    # todo: if it fails to download either file, use the previous day instead
    # todo: if the download succeeds clean old files
    # Download for day "t" will happen at night of day t-1, target_day will be
    # in the format "YYYYmmdd"
    target_day = (date.today() + timedelta(days=1)).strftime("%Y%m%d")

    with urllib.request.urlopen(ADMIE_LOAD_FORECAST_URL) as response:
        # Read the HTML as bytearray
        response_ba = response.read()

        # Decode to convert to string
        admie_soup = BeautifulSoup(response_ba.decode("utf-8"), 'html.parser')

    # Get the latest load forecast a tag
    load_forecast_a = \
        admie_soup.find(href=re.compile(
            target_day + "_" + LATEST_LOAD_FORECAST_SELECTOR))

    # If the latest was not yet available get the earliest
    if not load_forecast_a:
        load_forecast_a = \
            admie_soup.find(href=re.compile(
                target_day + "_" + EARLIEST_LOAD_FORECAST_SELECTOR))

    # Create the download link
    load_forecast_link = ADMIE_SITE_PREFIX + load_forecast_a["href"]

    # Directory to download daily forecast
    daily_target_dir = "../data/daily_forecast/"
    daily_file = daily_target_dir + target_day + "_DailyForecast.xlsx"

    # Download the file into the data directory
    urllib.request.urlretrieve(load_forecast_link, daily_file)

    # RES FORECAST todo: refactor download to a new function
    # Renewable energy infusion daily date
    res_forecast_a = admie_soup.find(href=re.compile(
        target_day + "_" + LATEST_RES_FORECAST_SELECTOR))

    # If the latest was not available yet get the earliest
    if not res_forecast_a:
        res_forecast_a = \
            admie_soup.find(href=re.compile(
                target_day + "_" + EARLIEST_RES_FORECAST_SELECTOR))

    # Create the res forecast download link
    res_forecast_link = ADMIE_SITE_PREFIX + res_forecast_a["href"]

    # Directory to download res daily forecast
    res_target_dir = "../data/res_forecast/"
    res_file = res_target_dir + target_day + "_RESForecast.xlsx"

    # Download the res forecast
    urllib.request.urlretrieve(res_forecast_link, res_file)

    # Parse forecast file and update json
    parse_forecast(daily_file, 'daily_forecast.json')

    # Parse res file and update json
    parse_forecast(res_file, 'res_forecast.json')


def parse_forecast(
        file,
        output_file,
        column_start=COLUMN_START,
        column_end=COLUMN_END):
    """
    Given an excel file extract the numerical values between the start and
    end indexes.

    Arguments:
        file(str): Complete file path including the filename of the excel
            file to be parsed.
        output_file (str): Output json file that should be updated
        column_start(int): Column from which the data begin.
        column_end(int): Column where the data end.

    Returns:
        Extracted values as a python list
    """

    # Date
    target_day = (date.today() + timedelta(days=1)).strftime("%Y%m%d")

    # Load workbook
    wb = op.load_workbook(file)

    # Get the active worksheet
    ws = wb.active

    # Get ranges of the values
    cell_range = ws[column_start: column_end]

    # Extract the values
    values = [cell.value for cell in cell_range[0]
              if isinstance(cell.value, float)]

    # Open file to add new values
    with open('../data/' + output_file, 'w+') as json_file:
        try:
            loaded_json = json.load(json_file)

            # Update the json dict
            loaded_json[target_day] = values

            # Update the file
            json.dump(loaded_json, json_file, indent=4)

        # First time running, create the file
        except json.JSONDecodeError:
            json.dump({target_day: values}, json_file, indent=4)


if __name__ == "__main__":
    download_daily_forecast()
