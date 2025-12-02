import schedule
import time
from .autoclose_overdue import autoclose_overdue

def run_scheduler():
    schedule.every().day.at("00:00").do(autoclose_overdue)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()