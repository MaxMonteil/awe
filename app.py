from flask import Flask, request, send_file, jsonify, render_template
import engine
import requests
import subprocess
import os

app = Flask(
    __name__,
    static_folder="dist/static",
    template_folder="dist",
)

ROOT_DIR = os.getcwd()
OUTPUT_DIR = ROOT_DIR + "/results/"


@app.route("/api/analyze")
def get_url():
    target_url = request.args.get("url", default="", type=str)
    output_format = request.args.get("output", default="json", type=str)

    # Ensure a valid format is given if not, defaults to json
    if output_format not in ["html", "json"]:
        output_format = "json"

    OUTPUT_FILE = OUTPUT_DIR + "parsed_audit." + output_format

    print("Calling lighthouse")
    subprocess.call(
        ["bash", f"{ROOT_DIR}/run_lighthouse.sh", target_url, output_format],
        bufsize=0,
    )

    if output_format == "html":
        print("Sending html file")
        return send_file(OUTPUT_FILE)

    audit = ""
    print("Reading json output")
    with open(OUTPUT_FILE, "r") as auditFile:
        audit = auditFile.read()
    eng = engine.Engine(audit_data=audit)

    print("Returning json output")
    return jsonify(eng.lhAudit.get_audit_data()), 200


@app.route("/api/crawl")
def crawl():
    target_url = request.args.get("url", default="", type=str)
    render = request.args.get("render", default=1, type=int)

    subprocess.call(
        ["node", f"{ROOT_DIR}/engine/crawler/crawler.js", target_url, OUTPUT_DIR], bufsize=0
    )

    if render:
        return send_file(f"{OUTPUT_DIR}/output.html")
    else:
        subprocess.call(
            [
                "cp",
                f"{OUTPUT_DIR}/output.html",
                f"{OUTPUT_DIR}/output.txt",
            ],
            bufsize=0,
        )
        return send_file(f"{OUTPUT_DIR}/output.txt")


@app.route("/", defaults={"path": ""})
#@app.route("/<path:path>")
def catch_all(path):
    if app.debug:
        return requests.get(f"http://localhost:8080/{path}").text
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
