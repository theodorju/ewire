import json
import urllib.request
import re
import openpyxl as op
from bs4 import BeautifulSoup
from datetime import date, timedelta
from Globals import ADMIE_SITE_PREFIX, ADMIE_LOAD_FORECAST_URL, \
    LATEST_LOAD_FORECAST_SELECTOR, EARLIEST_LOAD_FORECAST_SELECTOR, \
    DAILY_COLUMN_START, DAILY_COLUMN_END


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

    # Directory to download
    target_dir = "data/daily_forecast/"
    file = target_dir + target_day + "_DailyForecast.xlsx"

    # Download the file into the data directory
    urllib.request.urlretrieve(load_forecast_link, file)

    # Parse file and update json
    parse_daily_forecast(file)


def parse_daily_forecast(
        file,
        column_start=DAILY_COLUMN_START,
        column_end=DAILY_COLUMN_END):
    """
    Given an excel file extract the numerical values between the start and
    end indexes.

    Arguments:
        file(str): Complete file path including the filename of the excel
            file to be parsed.
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
    with open('data/daily_forecast.json', 'w+') as json_file:
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
