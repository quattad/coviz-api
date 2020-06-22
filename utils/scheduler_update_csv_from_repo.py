# import schedule
import time
from utils.update_csv_from_repo import update_csv_from_repo
# from threading import Timer
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

# def scheduler():
#     schedule.every().day.at("08:00").do(update_csv_from_repo)

#     while True:
#         print("Running scheduled check...")
#         schedule.run_pending()
#         time.sleep(3600)

# Scheduler with Time
# def scheduler():
#     print("Starting scheduler...")
#     Timer(interval=0.0, function=update_csv_from_repo).start()
#     time.sleep(3600)

def scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=update_csv_from_repo,
        trigger=IntervalTrigger(minutes=1),
        id='update_csv_from_repo',
        replace_existing=True
    )

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())