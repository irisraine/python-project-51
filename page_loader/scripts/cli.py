#!/usr/bin/env python

import argparse
import os
from page_loader import download


def main():
    parser = argparse.ArgumentParser(
        description="Downloads a webpage "
                    "and places it in the local directory "
                    "for offline viewing"
    )
    parser.add_argument(
        "-o",
        "--output",
        default=os.getcwd(),
        help="Path to the destination directory. "
             "The directory must be present and writable"
    )
    parser.add_argument("url", help="Source url")
    parser.add_argument(
        "-g",
        "--globalassets",
        action="store_true",
        help="If activated, page loader will download all assets, not only local ones"
    )
    parser.add_argument(
        "-l",
        "--log",
        action="store_true",
        help="Enable writing log file"
    )
    args = parser.parse_args()
    print(download(args.url, args.output, args.globalassets, args.log))


if __name__ == '__main__':
    main()
