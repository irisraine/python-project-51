#!/usr/bin/env python

import argparse
import os
import sys
import requests
import logging
from page_loader import download


def main():  # noqa: C901
    parser = argparse.ArgumentParser(
        description="Downloads a webpage "
                    "and places it in the local directory "
                    "for offline viewing."
    )
    parser.add_argument(
        "-o",
        "--output",
        default=os.getcwd(),
        help="Path to the destination directory. "
             "The directory must be present and writable. "
             "Leave it blank if you want to save the destination page "
             "into you current working directory"
    )
    parser.add_argument("url", help="Source url")
    parser.add_argument(
        "-g",
        "--globals",
        action="store_true",
        help="If activated, page loader utility will download "
             "all of requested page's associated resources, "
             "not only local ones."
    )
    parser.add_argument(
        "-l",
        "--log",
        action="store_true",
        help="Enable writing a log-file for a deep status inspection."
    )
    args = parser.parse_args()

    try:
        save_location = download(args.url, args.output, args.globals, args.log)
        print(f"The requested webpage has been successfully downloaded "
              f"into {save_location}")
        sys.exit(0)
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


if __name__ == '__main__':
    main()
