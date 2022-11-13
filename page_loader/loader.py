import os
import re
import requests
from bs4 import BeautifulSoup as bsoup
from urllib.parse import urlsplit
from requests.exceptions import ConnectionError


def download(url, save_dir_path):
    if not os.path.isdir(save_dir_path):
        return "Destination directory doesn't exist!"
    try:
        page = requests.get(url)
        if not page.ok:
            return "Requested web page is unavailable!"
    except ConnectionError:
        return "Connection error occurred!"
    filepath = os.path.join(save_dir_path, get_filename(url))
    with open(filepath, "w") as page_saved:
        page_saved.write(page.content.decode(page.encoding))
    return filepath


def get_filename(url):
    domain, path, params = urlsplit(url.rstrip("/"))[1:4]
    path = os.path.splitext(path)[0]
    filename = re.sub(r"[^A-Za-z0-9]", r"-", f'{domain}{path}{params}')
    return f'{filename}.html'
