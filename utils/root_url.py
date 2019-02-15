import re

def get_root_url(request_url):
    root_url_regex = r"((https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6})(?:\/(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)?)?)"
    return re.match(root_url_regex, request_url).groups(1)[1]
