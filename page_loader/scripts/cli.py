#!/usr/bin/env python

import argparse
import os
import sys
from page_loader import download


def main():
    parser = argparse.ArgumentParser(
        description="Downloads a webpage and places it in the local directory for offline viewing."  # noqa: E501
    )
    parser.add_argument(
        "-o",
        "--output",
        default=os.getcwd(),
        help="Path to the destination directory. The directory must be present and writable. "  # noqa: E501
             "Leave it blank if you want to save the destination page into you current working directory"  # noqa: E501
    )
    parser.add_argument("url", help="Source url")
    parser.add_argument(
        "-g",
        "--globals",
        action="store_true",
        help="If activated, page loader utility will download "
             "all of requested page's associated resources, not only local ones."  # noqa: E501
    )
    parser.add_argument(
        "-l",
        "--log",
        action="store_true",
        help="Enable writing a log-file for a deep status inspection."
    )
    args = parser.parse_args()
    save_location = download(args.url, args.output, args.globals, args.log)
    print(f"The requested webpage has been successfully downloaded into {save_location}")  # noqa: E501
    sys.exit(0)


if __name__ == '__main__':
    main()
