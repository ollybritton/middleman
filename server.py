from flask import Flask, request, render_template
from bs4 import BeautifulSoup

import requests
import urllib
import json
import time

from fix_document import fix_document, request_root

app = Flask(__name__)


def get_url_mappings():
    with open("url_tags.json", "r") as f:
        return json.loads(f.read())


def get_script_to_insert():
    with open("proxy.js", "r") as f:
        return f.read()


@app.route("/<path:url>")
def get_url(url):
    root_url = request_root(url)
    data = requests.get(url)

    document = BeautifulSoup(data.text, "html.parser")

    tags = get_url_mappings()

    for tag in list(tags.keys()):
        tags_in_document = document.find_all(tag)
        tag_attributes = tags[tag]

        for existing_tag in tags_in_document:
            for attribute in tag_attributes:
                try:
                    new_attribute_url = urllib.parse.urljoin(
                        root_url, existing_tag[attribute])
                    existing_tag[attribute] = new_attribute_url

                except KeyError:
                    pass

    script = document.new_tag(
        "script"
    )

    script.string = get_script_to_insert()

    document.body.append(script)
    return document.prettify()


if __name__ == '__main__':
    app.run(port=8000)
