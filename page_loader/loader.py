import re
import logging
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
from urllib.parse import urlsplit, urljoin
from page_loader.error_handler import error_handler
from page_loader.logger import init_logger
from page_loader.engine import get_http_request
from page_loader.engine import save, get_asset_name, create_dir, check_dir


@error_handler
def download(url, save_location, is_globals=False, is_logfile=False):
    init_logger(is_logfile)
    check_dir(save_location)
    logging.info("Session started. Trying to make a connection...")
    page = get_http_request(url)
    page_parsed = BeautifulSoup(page, 'html.parser')
    logging.info("Start downloading the requested page "
                 "and all of its associated resources.")
    bar = IncrementalBar('Downloading: ', max=1)
    elements = page_parsed.find_all(['img', 'link', 'script'])
    omitted_assets = 0
    if elements:
        assets_directory = create_dir(url, save_location)
        assets_source = get_assets(elements, url, assets_directory, is_globals)
        bar.max += len(assets_source)
        for asset_url_raw in assets_source.keys():
            asset_url_full = urljoin(url, asset_url_raw)
            asset = get_http_request(asset_url_full, is_asset=True)
            if asset:
                save(asset_url_full, assets_directory, asset, is_asset=True)
                bar.next()
            else:
                omitted_assets += 1
        replace_links(elements, assets_source)
        page = page_parsed.prettify()
    saved_page_fullname = save(url, save_location, page)
    bar.next()
    bar.finish()
    if omitted_assets:
        logging.info(f"{omitted_assets} resource file(s) "
                     f"has been omitted due to their unavailability.")
    return saved_page_fullname


def get_assets(elements, url, save_location, is_globals):
    assets_source = {}
    for element in elements:
        asset_url_orig = element.get(get_attribute(element))
        if asset_url_orig:
            asset_url_full = urljoin(url, asset_url_orig)
            if not is_globals:
                if urlsplit(url).netloc != urlsplit(asset_url_full).netloc:
                    continue
            if not re.match("(http|https)", asset_url_full):
                continue
            asset_local = get_asset_name(asset_url_full, save_location)
            assets_source.setdefault(asset_url_orig, asset_local)
    return assets_source


def replace_links(elements, assets_source):
    for element in elements:
        attribute = get_attribute(element)
        asset_source = element.get(attribute)
        if asset_source and assets_source.get(element[attribute]):
            element[attribute] = element[attribute].replace(
                element[attribute],
                assets_source[element[attribute]]
            )


def get_attribute(asset):
    asset_all_types = {
        "img": "src",
        "link": "href",
        "script": "src"
    }
    return asset_all_types[asset.name]
