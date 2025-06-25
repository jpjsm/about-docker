import json
import os
import urllib3
import datetime
import threading
from time import sleep

from flask import Flask
app = Flask(__name__)

servername = "rest02"
othername = "rest01"
otherport = 10067

waittimeseconds = 10

@app.route('/')
def hello():
    return f"Welcome to server {servername}\n"

@app.route('/rest02-to-rest01')
def getFromOther():
    http = urllib3.PoolManager()
    response = http.request("GET", f"http://{othername}:{otherport}/")

    status = response.status
    data = response.data.decode("utf-8")
    return f"In server {servername}\nreply from other server: [{status}] {data}"

def writeFile():
    content = str(int(datetime.datetime.utcnow().timestamp()*1000))
    filename = f"/opt/data/{content}.txt" 
    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

    print(f"DEBUG   [rest02.py].[writeFile] Wrote file {filename} with content {content}")

def writeFiles():
    global waittimeseconds
    while True:
        writeFile()
        sleep(waittimeseconds)
        print("DEBUG   [rest02.py].[writeFiles] feeling rested")

if __name__ == '__main__':
    daemon = threading.Thread(target=writeFiles, daemon=True, name="Write_Files")
    daemon.start()
    app.run(host ='0.0.0.0', port = 10069, debug = True)  