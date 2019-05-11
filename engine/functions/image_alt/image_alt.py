""""
Analyzes a list of image tags and returns them with an alt attribute describing the
image's content.
"""

from bs4 import BeautifulSoup
from google.cloud import vision
from google.cloud.vision import types


def run(tag_data):
    snippet = tag_data["snippet"]

    # Modifications to the BeautifulSoup tag
    #soup = BeautifulSoup(str(snippet),"html.parser")
    snippet["alt"] = _annotate_image(_analyze_image(snippet.get("src")))

    tag_data["snippet"] = snippet
    return tag_data


def _analyze_image(path):
    """Returns web annotations given the path to an image."""
    client = vision.ImageAnnotatorClient()

    if path.startswith("http") or path.startswith("gs:"):
        image = types.Image()
        image.source.image_uri = path
    else:
        with open(path, "rb") as image_file:
            content = image_file.read()

        image = types.Image(content=content)

    return client.web_detection(image=image).web_detection


def _annotate_image(annotations):
    """Prints detected features in the provided web annotations."""
    alt = ""
    if annotations.pages_with_matching_images:
        for entity in annotations.web_entities:
            alt += entity.description + " "
    else:
        alt="image"

    return alt

print(_annotate_image(_analyze_image("http://lobulate-retirement.000webhostapp.com/awe/images/1.jpg")))
