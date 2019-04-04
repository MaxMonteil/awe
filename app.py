import engine
from flask import Flask, request, send_file, jsonify, render_template
import subprocess

app = Flask(
    __name__,
    static_folder="dist/static",
    template_folder="dist",
)

ROOT_DIR = "/var/www/awe/"
OUTPUT_DIR = ROOT_DIR + "/results/"


@app.route("/api/")
def get_url():
    target_url = request.args.get("url", default="", type=str)
    output_format = request.args.get("output", default="json", type=str)

    # Ensure a valid format is given if not, defaults to json
    if output_format not in ["html", "json"]:
        output_format = "json"

    OUTPUT_FILE = OUTPUT_DIR + output_format

    subprocess.call(
        ["sudo", "bash", f"{ROOT_DIR}run_lighthouse.sh", target_url, output_format],
        bufsize=0,
    )

    if output_format is "html":
        return send_file(OUTPUT_FILE)

    audit = ""
    with open(OUTPUT_FILE, "r") as auditFile:
        audit = auditFile.read()

    eng = engine.Engine(audit_data=audit)

    return jsonify(eng.lhAudit.get_audit_data()), 200


@app.route("/api/crawl")
def crawl():
    target_url = request.args.get("url", default="", type=str)
    render = request.args.get("render", default=1, type=int)

    subprocess.call(
        ["sudo", "node", "/var/www/awe/api/crawler/crawler.js", target_url], bufsize=0
    )

    if render:
        return send_file("/var/www/awe/api/output.html")
    else:
        subprocess.call(
            [
                "sudo",
                "cp",
                "/var/www/awe/api/output.html",
                "/var/www/awe/api/output.txt",
            ],
            bufsize=0,
        )
        return send_file("/var/www/awe/api/output.txt")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
