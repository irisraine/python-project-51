import os
import re
from urllib.parse import urlsplit


def get_base_name(url):
    netloc, path, query = urlsplit(url.rstrip("/"))[1:4]
    path = os.path.splitext(path)[0]
    base_name = re.sub(r"[\W_]", "-", f'{netloc}{path}{query}')
    return base_name


def get_asset_name(url, is_link):
    asset_name = get_base_name(url)
    extension = os.path.splitext(urlsplit(url).path)[-1]
    if not extension and is_link:
        extension = ".html"
    if len(asset_name) + len(extension) > 255:
        asset_name = asset_name[:255 - len(extension) - 1]
    return f'{asset_name}{extension}'
