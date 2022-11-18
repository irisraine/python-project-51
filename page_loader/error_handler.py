import sys
import requests
import logging


def error_handler(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except requests.ConnectionError:
            logging.error("Connection error occurred!")
            sys.exit(1)
        except requests.HTTPError:
            logging.error("Requested web page is unavailable!")
            sys.exit(1)
        except FileNotFoundError:
            logging.error("Destination directory doesn't exist!")
            sys.exit(1)
        except PermissionError:
            logging.error("Access violation!")
            sys.exit(1)
        except OSError:
            logging.error("Generic OS Error")
            sys.exit(1)
        return result
    return inner
