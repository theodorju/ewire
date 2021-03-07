from apscheduler.schedulers.background import BackgroundScheduler
from .Scrapper import download_daily_forecast


def prepare_file():
    """ Function for test purposes. """

    # Update daily forecast json file
    download_daily_forecast()


def start_scheduler():
    # Background scheduler to download and parse file
    job = BackgroundScheduler()

    # Scheduler will run daily at 1 AM
    job.add_job(prepare_file, 'cron', hour=1)
    job.start()
    print("Scheduler started.")
