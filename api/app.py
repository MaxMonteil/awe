from flask import Flask
from flask import request
import subprocess
from flask import send_file

app = Flask(__name__)

@app.route('/api/')
def getUrl():
    page = request.args.get('url', default = "", type = str)
    output = request.args.get('output', default = "json", type = str)
    subprocess.call(['sudo','bash','/var/www/awe/api/run.sh', page, output],bufsize=0)
    if (output=="html"):
        return send_file("/var/www/awe/api/result.html")
    else:
        subprocess.call(['python','/var/www/awe/api/LighthouseResponseParser/testAuditParsing.py'],bufsize=0)
        return send_file("/var/www/awe/api/testResults.json")

@app.route("/")
def hello():
    return "Hello from AWE!"
