import os
import re
import logging
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
from urllib.parse import urlsplit, urljoin
from page_loader.error_handler import error_handler
from page_loader.logger import init_logger
from page_loader.engine import make_http_request, save_html, save_asset, create_directory, get_asset_name


@error_handler
def download(url, save_location, is_global_assets=False, is_logfile=False):
    init_logger(is_logfile)
    check_location(save_location)
    logging.info("Session started.")
    logging.info(f"Trying to make connection to {url}.")
    page = make_http_request(url)
    page_parsed = BeautifulSoup(page, 'html.parser')
    logging.info("The connection is successful!")
    logging.info(f"Save location is {save_location}.")
    logging.info("Start downloading a page and all of its associated resources.")
    if get_elements(page_parsed):
        download_assets(page_parsed, url, save_location, is_global_assets)
        page = page_parsed.prettify()
    path_to_saved_page = save_html(url, save_location, page)
    logging.info("The requested webpage has been successfully saved!")
    return path_to_saved_page


def download_assets(soup, url, save_location, is_global_assets):
    directory_to_save = create_directory(url, save_location)
    assets_source = {}

    def is_local_asset(asset_url):
        return urlsplit(url).netloc == urlsplit(asset_url).netloc

    def is_valid_asset(asset_url):
        return re.match("(http|https)", asset_url)

    elements = get_elements(soup)
    for element in elements:
        asset_url_orig = element.get(get_attribute(element))
        if asset_url_orig:
            asset_url_full = urljoin(url, asset_url_orig)
            if not is_global_assets and not is_local_asset(asset_url_full):
                logging.warning(f"The resource {asset_url_full} cannot be saved in non-global mode")
                continue
            asset_local = get_asset_name(asset_url_full, directory_to_save)
            assets_source.setdefault(asset_url_orig, asset_local)
    bar = IncrementalBar('Downloading: ', max=len(assets_source))
    for asset_url_raw in assets_source.keys():
        asset_url_full = urljoin(url, asset_url_raw)
        if is_valid_asset(asset_url_full):
            asset = make_http_request(asset_url_full, is_asset=True)
            save_asset(asset_url_full, directory_to_save, asset)
        else:
            logging.warning(f"The resource {asset_url_full} has unrecognized format and has been omitted.")
        bar.next()
    bar.finish()
    for element in elements:
        attribute = get_attribute(element)
        asset_source = element.get(attribute)
        if asset_source:
            if not is_global_assets and not is_local_asset(asset_source):
                continue
            element[attribute] = element[attribute].replace(
                element[attribute],
                assets_source[element[attribute]]
            )


def get_elements(soup):
    return soup.find_all(['img', 'link', 'script'])


def get_attribute(asset):
    asset_all_types = {
        "img": "src",
        "link": "href",
        "script": "src"
    }
    return asset_all_types[asset.name]


def check_location(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError
