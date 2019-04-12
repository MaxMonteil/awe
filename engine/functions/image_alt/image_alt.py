# Takes list of img and return beautifulsoup objects
from bs4 import BeautifulSoup
import argparse
import io

from google.cloud import vision
from google.cloud.vision import types


def run(html):
	 htmlTags = [BeautifulSoup(item["snippet"], "html.parser").find() for item in html]
	 image(htmlTags)


def image(htmlSnippets):
	for tag in htmlSnippets:
			image=tag.find('img')
			src=tag.find('img').get('src')
			alt=report(annotate(src))
			image.set('alt',alt)

def annotate(path):
    """Returns web annotations given the path to an image."""
    client = vision.ImageAnnotatorClient()

    if path.startswith('http') or path.startswith('gs:'):
        image = types.Image()
        image.source.image_uri = path

    else:
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

    web_detection = client.web_detection(image=image).web_detection

    return web_detection


def report(annotations):
    """Prints detected features in the provided web annotations."""
    alt=""
    if annotations.pages_with_matching_images:
        # print('\n{} Pages with matching images retrieved'.format(
        #     len(annotations.pages_with_matching_images)))

        for entity in annotations.web_entities:
            alt+=entity.description+" "

            # print('Description: {}'.format(entity.description))
    return alt

