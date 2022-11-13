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
    args = parser.parse_args()
    print(download(args.url, args.output))


if __name__ == '__main__':
    main()
