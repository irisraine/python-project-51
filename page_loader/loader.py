import re
import logging
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
from urllib.parse import urlsplit, urljoin
from page_loader.logger import init_logger
from page_loader.network import get_http_request
from page_loader.io_engine import save_data, create_directory, check_directory
from page_loader.name_assigner import get_base_name, get_asset_name


def download(url, save_location, is_globals=False, is_logfile=False):
    init_logger(is_logfile)
    check_directory(save_location)
    logging.info("Session started.")
    print("Trying to make a connection...")
    page = get_http_request(url)
    page_parsed = BeautifulSoup(page, 'html.parser')
    print("Start downloading the requested page "
          "and all of its associated resources.")
    bar = IncrementalBar('Downloading: ', max=1)
    elements = page_parsed.find_all(['img', 'link', 'script'])
    omitted_assets = 0
    if elements:
        assets_directory = create_directory(url, save_location)
        logging.info(f"Directory {assets_directory} is created")
        assets_source = get_assets(elements, url, is_globals)
        bar.max += len(assets_source)
        for asset_url_orig, asset_local_name in assets_source.items():
            asset_url_full = urljoin(url, asset_url_orig)
            asset = get_http_request(asset_url_full, is_asset=True)
            if asset:
                save_data(asset_local_name, save_location, asset)
                logging.info(f"Associated resource {asset_url_full} "
                             f"has been downloaded.")
                bar.next()
            else:
                omitted_assets += 1
        replace_links(elements, assets_source)
        page = page_parsed.prettify()
    page_local_name = f'{get_base_name(url)}.html'
    saved_page_fullname = save_data(page_local_name, save_location, page)
    logging.info(f"The requested webpage {url} "
                 f"has been successfully downloaded.")
    bar.next()
    bar.finish()
    if omitted_assets:
        print(f"{omitted_assets} resource file(s) "
              f"has been omitted due to their unavailability.")
    return saved_page_fullname


def get_assets(elements, url, is_globals):
    assets_source = {}
    for element in elements:
        attribute = get_attribute(element)
        asset_url_orig = element.get(attribute)
        if asset_url_orig:
            asset_url_full = urljoin(url, asset_url_orig)
            if not is_globals:
                if urlsplit(url).netloc != urlsplit(asset_url_full).netloc:
                    continue
            if not re.match("(http|https)", asset_url_full):
                continue
            is_link = (attribute == "href")
            asset_filename = get_asset_name(asset_url_full, is_link)
            asset_local_name = f'{get_base_name(url)}_files/{asset_filename}'
            assets_source.setdefault(asset_url_orig, asset_local_name)
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
