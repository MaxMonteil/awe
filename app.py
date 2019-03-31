from awe import Engine
from flask import Flask, request, send_file, jsonify
import subprocess

app = Flask(__name__)
ROOT_DIR = "/var/www/awe/"
OUTPUT_DIR = ROOT_DIR + "/results/"


@app.route("/api/")
def getUrl():
    target_url = request.args.get("url", default="", type=str)
    output_format = request.args.get("output", default="json", type=str)

    # Ensure a valid format is given if not, defaults to json
    if output_format not in ["html", "json"]:
        output_format = "json"

    OUTPUT_FILE = OUTPUT_DIR + output_format

    subprocess.call(
        ["sudo", "bash", f"{ROOT_DIR}run.sh", target_url, output_format],
        bufsize=0,
    )

    if output_format is "html":
        return send_file(OUTPUT_FILE)

    audit = ""
    with open(OUTPUT_FILE, "r") as auditFile:
        audit = auditFile.read()

    engine = Engine(audit_data=audit)

    return jsonify(engine.lhAudit.get_audit_data()), 200


@app.route("/")
def hello():
    return "Hello from AWE!"
