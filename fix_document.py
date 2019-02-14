from bs4 import BeautifulSoup
import requests
import re

url_patterns = {
    # Attempts to find the HTTP/HTTPS prefix.
    "http_section": r"(https?):\/\/",

    # https://google.com, http://www.example.org/awesome
    "full_url": r"(https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}(?:\/(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)?)",

    # //code.jquery.com, //google.com/awesome
    "double_slash_url": r"(\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}(?:\/(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)?)",

    # google.com, example.org/awesomer
    "httpless_url": r"((?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.(?!js|css|html|xml|xhtml)[a-z]{2,6}(?:\/(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)?)",

    # /script.js, /css.css
    "slash_resource_name": r"\/([-a-zA-Z0-9@:%._\+~#=]{2,256}\.(?:js|css|html|xml|xhtml))",

    # script.js, css.css
    "resource_name": r"([-a-zA-Z0-9@:%._\+~#=]{2,256}\.(?:js|css|html|xml|xhtml))",

    # Any type of URL. TODO: THIS IS A MONSTER, and should probably be fixed.
    "any": r"(?:(https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}(?:\/(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)?))|(?:(\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}(?:\/(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)?))|(?:((?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.(?!js|css|html|xml|xhtml)[a-z]{2,6}(?:\/(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)?))|(?:\/([-a-zA-Z0-9@:%._\+~#=]{2,256}\.(?:js|css|html|xml|xhtml)))|(?:([-a-zA-Z0-9@:%._\+~#=]{2,256}\.(?:js|css|html|xml|xhtml)))",

    "root_url": r"((https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6})(?:\/(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)?)",
}


def convert_to_full_url(url, root_url):
    converted_urls = []

    # Put a slash on end of base url if it doesn't have it.
    root_url = root_url + '/' if root_url[-1] != "/" else root_url
    root_url = re.sub(url_patterns["http_section"], r"http://", root_url)

    # First convert URL to HTTP:
    converted = re.sub(url_patterns["http_section"], r"http://", url)
    converted_urls.append(converted)

    # Put HTTP in front of URLs with double slashes:
    converted = re.sub(url_patterns["double_slash_url"], r"http:\g<1>", url)
    converted_urls.append(converted)

    # Put HTTP:// in front of URLs without them.
    converted = re.sub(url_patterns["httpless_url"], r"http://\g<1>", url)
    converted_urls.append(converted)

    # Put the document root in front of urls without the document root that have a slash in front of them.
    converted = re.sub(url_patterns["slash_resource_name"],
                       rf"{root_url}\g<1>", url)
    converted_urls.append(converted)

    # Put the document root url in from of urls without the document root that don't have a slash in front of them.
    converted = re.sub(url_patterns["resource_name"], rf"{root_url}\g<1>", url)
    converted_urls.append(converted)

    return [x for x in converted_urls if x != url][0]


def convert_url(url, prefix="localhost:5000/url/"):
    return prefix + url


def request_root(request_url):
    return re.match(url_patterns["root_url"], request_url).groups(1)[1]


def fix_document(document, root_url, prefix="localhost:5000/url/"):
    document = re.sub(
        url_patterns["any"],
        # lambda match, root_url=root_url: convert_to_full_url(match, root_url),
        lambda match, root_url=root_url: convert_to_full_url(
            match[0], root_url),
        document,

        flags=re.MULTILINE
    )

    document = re.sub(
        url_patterns["full_url"],
        lambda match, prefix=prefix: convert_url(match[0], prefix),
        document,

        flags=re.MULTILINE
    )

    return document


if __name__ == "__main__":
    print(
        fix_document(
            """<script src='script.js'></script>
            <link rel='stylesheet' href='https://google.com/styles.css' />""",
            "https://google.com",
            "localhost:5000/"
        )
    )
