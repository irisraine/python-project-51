import os
import re
import requests
from urllib.parse import urlsplit

PATH_PATTERN = "[^A-Za-z0-9]"
ASSET_TYPES = {
    "img": "src",
    "link": "href",
    "script": "src"
}


def make_http_request(url, is_asset=False):
    response = requests.get(url)
    if not response.ok:
        response.raise_for_status()
    if is_asset:
        return response.content
    encoding = response.encoding
    return response.content.decode(encoding)


def save_html(url, save_location, content):
    filename = f'{get_base_name(url)}.html'
    absolute_filename = os.path.join(save_location, filename)
    with open(absolute_filename, 'w') as current_file:
        current_file.write(content)
    return absolute_filename


def save_asset(url, save_location, content):
    filename = get_asset_name(url, save_location)
    absolute_filename = os.path.join(save_location, filename)
    with open(absolute_filename, 'wb') as current_file:
        current_file.write(content)
    return absolute_filename


def create_directory(url, save_location):
    directory = os.path.join(save_location, f'{get_base_name(url)}_files')
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory


def get_base_name(url):
    netloc, path, query = urlsplit(url.rstrip("/"))[1:4]
    path = os.path.splitext(path)[0]
    base_name = re.sub(PATH_PATTERN, "-", f'{netloc}{path}{query}')
    return base_name


def get_asset_name(url, save_location):
    asset_name = get_base_name(url)
    extension = os.path.splitext(urlsplit(url).path)[-1]
    if len(asset_name) + len(extension) > 255:
        asset_name = asset_name[:255 - len(extension) - 1]
    return f'{save_location}/{asset_name}{extension}'


