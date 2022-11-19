import re
import logging
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
from urllib.parse import urlsplit, urljoin
from page_loader.error_handler import error_handler
from page_loader.logger import init_logger
from page_loader.engine import make_http_request, save_html, save_asset, create_directory, get_asset_name, check_location


@error_handler
def download(url, save_location, is_global_assets=False, is_logfile=False):
    init_logger(is_logfile)
    check_location(save_location)
    logging.info(f"Session started. Trying to make a connection...")
    page = make_http_request(url)
    page_parsed = BeautifulSoup(page, 'html.parser')
    logging.info("Start downloading a page and all of its associated resources.")
    bar = IncrementalBar('Downloading: ', max=1)
    elements = get_elements(page_parsed)
    omitted_assets = 0
    if elements:
        directory_to_save = create_directory(url, save_location)
        assets_source = get_assets(elements, url, directory_to_save, is_global_assets)
        bar.max += len(assets_source)
        for asset_url_raw in assets_source.keys():
            asset_url_full = urljoin(url, asset_url_raw)
            asset = make_http_request(asset_url_full, is_asset=True)
            if asset:
                save_asset(asset_url_full, directory_to_save, asset)
                bar.next()
            else:
                omitted_assets += 1
        replace_links(elements, assets_source)
        page = page_parsed.prettify()
    path_to_saved_page = save_html(url, save_location, page)
    bar.next()
    bar.finish()
    if omitted_assets:
        logging.info(f"{omitted_assets} resource file(s) has been omitted due to their unavailability.")
    return path_to_saved_page


def get_assets(elements, url, save_location, is_global_assets):
    assets_source = {}

    def is_local_asset(asset_url):
        return urlsplit(url).netloc == urlsplit(asset_url).netloc

    def is_valid_asset(asset_url):
        return re.match("(http|https)", asset_url)

    for element in elements:
        asset_url_orig = element.get(get_attribute(element))
        if asset_url_orig:
            asset_url_full = urljoin(url, asset_url_orig)
            if not is_global_assets and not is_local_asset(asset_url_full):
                continue
            if not is_valid_asset(asset_url_full):
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


def get_elements(soup):
    return soup.find_all(['img', 'link', 'script'])


def get_attribute(asset):
    asset_all_types = {
        "img": "src",
        "link": "href",
        "script": "src"
    }
    return asset_all_types[asset.name]

