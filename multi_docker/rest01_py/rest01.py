import json
import os
import shutil
import urllib3
import threading

from flask import Flask
app = Flask(__name__)

servername = "rest01"
othername = "rest02"
otherport = 10069

sourceData = '/opt/data/'
readingArea = '/tmp/reading-area'
deleteMe = '/tmp/delete-me'

@app.route('/')
def hello():
    return f"Welcome to server {servername}\n"

@app.route('/rest01-to-rest02')
def getFromOther():
    http = urllib3.PoolManager()
    response = http.request("GET", f"http://{othername}:{otherport}/")

    status = response.status
    data = response.data.decode("utf-8")
    return f"In server {servername}\nreply from other server: [{status}] {data}"

@app.route('/get-files')
def getFiles():
    os.makedirs(readingArea, 777, True)
    os.makedirs(deleteMe, 777, True)

    for currentFileName in os.listdir(sourceData):
        currentFilePath = os.path.join(sourceData, currentFileName)
        shutil.move(currentFilePath,readingArea)

    reply = dict()
    for currentFileName in os.listdir(readingArea):
        currentFilePath = os.path.join(readingArea, currentFileName)
        with open(currentFilePath, 'r', encoding='utf-8') as inputfile:
            content = inputfile.read()
            reply[currentFileName] = content

        shutil.move(currentFilePath, deleteMe)

    daemon = threading.Thread(target=deleteReadFiles, daemon=True, name="Delete_Files")
    daemon.start()

    return json.dumps(reply)

def deleteReadFiles():
    for currentFileName in os.listdir(deleteMe):
        currentFilePath = os.path.join(deleteMe, currentFileName)
        os.remove(currentFilePath)

if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 10067, debug = True)  