import sys
import requests
import logging


def error_handler(func):  # noqa: C901
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except requests.Timeout:
            logging.error("The request is timed out.")
            sys.exit(1)
        except requests.ConnectionError:
            logging.error("General connection error occurred.")
            print("Please check your internet-connection and try again")
            sys.exit(1)
        except requests.HTTPError:
            logging.error("Requested web resource is unavailable.")
            sys.exit(1)
        except FileNotFoundError:
            logging.error("Destination directory doesn't exist.")
            print("Enter the correct path to save directory, "
                  "or use the default path")
            sys.exit(1)
        except NotADirectoryError:
            logging.error("The destination path "
                          "doesn't correspond to a directory")
            sys.exit(1)
        except PermissionError:
            logging.error("Access violation.")
            print("You have no permission to save file in this location")
            sys.exit(1)
        except OSError:
            logging.critical("General file system error.")
            sys.exit(1)
        return result
    return inner
