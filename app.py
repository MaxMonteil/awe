from engine import Engine
from flask import Flask, request, send_file, jsonify, render_template
from pathlib import Path
import os
import requests
import asyncio
import logging


try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
finally:
    asyncio.get_child_watcher().attach_loop(loop)

app = Flask(__name__, static_folder="dist/static", template_folder="dist")

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('this will show in the log')

ROOT_DIR = Path(os.environ.get("ROOT_DIR") or Path.cwd())
OUTPUT_DIR = Path(ROOT_DIR, "results/")


@app.route("/api/analyze")
def get_analysis():
    target_url = request.args.get("url", default="", type=str)
    output_format = request.args.get("output", default="json", type=str)

    # Ensure a valid format is given if not, defaults to json
    if output_format not in ("html", "json"):
        output_format = "json"

    print(f"Calling lighthouse on {target_url}")
    engine = Engine(target_url=target_url)

    asyncio.set_event_loop(loop)
    loop.run_until_complete(engine.run_analysis())

    print("Sending analysis")
    if output_format == "json":
        return jsonify(engine.audit), 200
    else:
        return (
            send_file(
                engine.audit,
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

    asyncio.set_event_loop(loop)
    loop.run_until_complete(engine.run_crawler())

    return (
        send_file(
            engine.site_html,
            as_attachment=True,
            attachment_filename="awe_site_crawl.html",
        ),
        200,
    )


@app.route("/api/run_engine")
def awe():
    target_url = request.args.get("url", default="", type=str)

    engine = Engine(target_url=target_url)

    asyncio.set_event_loop(loop)
    loop.run_until_complete(engine.run_engine())

    return (
        send_file(
            engine.accessible_site,
            as_attachment=True,
            attachment_filename="awe_site.html"
        ),
        200,
    )


@app.route("/", defaults={"path": ""})
# @app.route("/<path:path>")
def catch_all(path):
    if app.debug:
        return requests.get(f"http://localhost:8080/{path}").text
    return render_template("index.html")

@app.route("/contact", defaults={"path": ""})
# @app.route("/<path:path>")
def contact(path):
    if app.debug:
        return requests.get(f"http://localhost:8080/{path}").text
    return render_template("contact.html")

@app.route("/about", defaults={"path": ""})
# @app.route("/<path:path>")
def about(path):
    if app.debug:
        return requests.get(f"http://localhost:8080/{path}").text
    return render_template("about.html")

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0" if os.environ.get("ON_GCP") else None,
        port=80 if os.environ.get("ON_GCP") else None,
)


