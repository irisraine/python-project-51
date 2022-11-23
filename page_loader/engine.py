import os
import re
import logging
import requests
from urllib.parse import urlsplit


def get_http_request(url, is_asset=False):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text if not is_asset else response.content
    except requests.RequestException as error:
        if not is_asset:
            raise error
        logging.warning(f"Associated resource {url} is unavailable.")


def save(local_name, save_location, content, is_asset=False):
    mode = 'w' if not is_asset else 'wb'
    absolute_filename = os.path.join(save_location, local_name)
    with open(absolute_filename, mode) as current_file:
        current_file.write(content)
    return absolute_filename


def create_directory(url, save_location):
    directory = os.path.join(save_location, f'{get_base_name(url)}_files')
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory


def check_directory(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError
    if not os.path.isdir(directory):
        raise NotADirectoryError


def get_base_name(url):
    netloc, path, query = urlsplit(url.rstrip("/"))[1:4]
    path = os.path.splitext(path)[0]
    base_name = re.sub(r"[\W_]", "-", f'{netloc}{path}{query}')
    return base_name


def get_page_name(url):
    return f'{get_base_name(url)}.html'


def get_directory_name(url):
    return f'{get_base_name(url)}_files'


def get_asset_name(url, is_link):
    asset_name = get_base_name(url)
    extension = os.path.splitext(urlsplit(url).path)[-1]
    if not extension and is_link:
        extension = ".html"
    if len(asset_name) + len(extension) > 255:
        asset_name = asset_name[:255 - len(extension) - 1]
    return f'{asset_name}{extension}'
