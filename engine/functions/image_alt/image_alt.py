"""
Analyzes a list of image tags and returns them with an alt attribute describing the
image's content.
"""

from bs4 import BeautifulSoup
from google.cloud import vision
from google.cloud.vision import types


def run(failing_items):
    paths = [item["path"] for item in failing_items]
    tags = [BeautifulSoup(item["snippet"], "html.parser") for item in failing_items]

    for tag in tags:
        tag.img.set("alt", _annotate_image(_analyze_image(tag.img.get("src"))))

    return [{"snippet": snippet, "path": path} for snippet, path in zip(tags, paths)]


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
        # print('\n{} Pages with matching images retrieved'.format(
        #     len(annotations.pages_with_matching_images)))

        for entity in annotations.web_entities:
            alt += entity.description + " "

            # print('Description: {}'.format(entity.description))
    return alt
