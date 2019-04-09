from engine import Engine
from flask import Flask, request, send_file, jsonify, render_template
from pathlib import Path
import os
import requests
import asyncio

app = Flask(__name__, static_folder="dist/static", template_folder="dist")

ROOT_DIR = Path(os.environ.get("ROOT_DIR") or Path.cwd())
OUTPUT_DIR = Path(ROOT_DIR, "results/")


@app.route("/api/analyze")
def get_analysis():
    target_url = request.args.get("url", default="", type=str)
    output_format = request.args.get("output", default="json", type=str)

    # Ensure a valid format is given if not, defaults to json
    if output_format not in ("html", "json"):
        output_format = "json"

    print("Calling lighthouse")
    engine = Engine(target_url=target_url)
    asyncio.run(engine.run_analysis())

    print("Sending analysis")
    if output_format == "json":
        return jsonify(engine.get_full_audit_data()), 200
    else:
        return (
            send_file(
                engine.get_full_audit_data(),
                as_attachment=True,
                attachment_filename=f"awe_analysis.{output_format}",
            ),
            200,
        )


@app.route("/api/crawl")
def crawl():
    target_url = request.args.get("url", default="", type=str)

    print("Calling crawler")
    engine = Engine(target_url=target_url)
    asyncio.run(engine.run_crawler())

    return (
        send_file(
            engine.get_html(),
            as_attachment=True,
            attachment_filename="awe_site_crawl.html",
        ),
        200,
    )


@app.route("/", defaults={"path": ""})
# @app.route("/<path:path>")
def catch_all(path):
    if app.debug:
        return requests.get(f"http://localhost:8080/{path}").text
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
