import logging
import requests


def get_http_request(url, is_asset=False):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text if not is_asset else response.content
    except requests.RequestException as error:
        if not is_asset:
            raise error
        logging.warning(f"Associated resource {url} is unavailable.")
