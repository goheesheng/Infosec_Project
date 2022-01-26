from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import atexit
try:
    print('s')
except SSL

sched = BackgroundScheduler(daemon=True)
# sched.add_job(sensor,'interval',seconds=3)
sched.start()

@sched.scheduled_job('interval',seconds=3)
def sensor():
    """ Function for test purposes. """
    print("Scheduler is alive!")
app = Flask(__name__)

@app.route("/home")
def home():
    """ Function for test purposes. """
    return "Welcome Home :) !"

if __name__ == "__main__":
    # atexit.register(lambda: sched.shutdown(wait=False))
    
    app.run()


# import atexit

# # v2.x version - see https://stackoverflow.com/a/38501429/135978
# # for the 3.x version
# from apscheduler.schedulers.background import BackgroundScheduler
# from flask import Flask

# app = Flask(__name__)

# cron = BackgroundScheduler(daemon=True)
# # Explicitly kick off the background thread
# cron.start()

# @cron.interval_schedule(seconds=3)
# def job_function():
#     # Do your work here
#     print('testjob')

# # Shutdown your cron thread if the web process is stopped
# atexit.register(lambda: cron.shutdown(wait=False))

# if __name__ == '__main__':
#     app.run()