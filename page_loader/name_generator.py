import os
import re
from urllib.parse import urlsplit

PATH_PATTERN = "[^A-Za-z0-9]"
REPLACER = "-"


def get_local_name(url):
    domain, path, params = urlsplit(url.rstrip("/"))[1:4]
    path = os.path.splitext(path)[0]
    filename = re.sub(PATH_PATTERN, REPLACER, f'{domain}{path}{params}')
    return filename


def get_asset_name(url, asset_url_full):
    asset_name = get_local_name(asset_url_full)
    extension = os.path.splitext(urlsplit(asset_url_full).path)[-1]
    if len(asset_name) + len(extension) > 255:
        asset_name = asset_name[:255 - len(extension) - 1]
    return f'{get_local_name(url)}_files/{asset_name}{extension}'

