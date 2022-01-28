from flask import Flask, request, render_template, g, redirect, url_for, flash, session,send_from_directory
import time
from queue import Queue
from multiprocessing import Process
import subprocess
import sys
import os
some_queue = None

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret key"
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(),'saved')

@app.route('/restart')
def restart():
    some_queue.put("something")
    return "Quit"

def start_flaskapp(queue):
   some_queue = queue
   app.run()

if __name__  == "__main__":
    q = Queue()
    p = Process(target=start_flaskapp, args=[q,])
    p.start()
    while True: #wathing queue, sleep if there is no call, otherwise break
        if q.empty(): 
                time.sleep(1)
        else:
            break
    p.terminate() #terminate flaskapp and then restart the app on subprocess
    args = [sys.executable] + [sys.argv[0]]
    subprocess.call(args)