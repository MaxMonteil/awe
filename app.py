from flask import Flask, request, send_file
import subprocess

app = Flask(__name__)


@app.route("/api/")
def getUrl():
    page = request.args.get("url", default="", type=str)
    out_format = request.args.get("output", default="json", type=str)
    subprocess.call(["sudo", "bash", "/var/www/awe/run.sh", page, out_format], bufsize=0)
    if (out_format == "html"):
        return send_file("/var/www/awe/results/result.html")
    else:
        subprocess.call(["python", "/var/www/awe/lighthouseparser/testAuditParsing.py"], bufsize=0)
        return send_file("/var/www/awe/api/testResults.json")


@app.route("/")
def hello():
    return "Hello from AWE!"
