#!/usr/bin/python
# -*- coding: utf-8 -*-


from mutagenerate.core import ID3, AmazonSource
from mutagenerate.log import logging, logger

import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

from optparse import OptionParser

parser = OptionParser()
parser.add_option("", "--directory", dest="directory", default="", help="Directory")
parser.add_option("", "--filename", dest="filename", default="", help="filename")
parser.add_option("", "--cache", dest="cache", default="", help="cache")
parser.add_option("", "--update", dest="update", default=False, action="store_true", help="Update existing frames")
parser.add_option("", "--yes", dest="yes", default=False, action="store_true", help="Say yes to saving")
options, args = parser.parse_args()


if __name__ == "__main__":
    if options.cache:
        try:
            import requests_cache
            requests_cache.install_cache(options.cache)
        except ImportError as e:
            logger.warning("Cannot set cache, install requests_cache first")
    id3s = []
    if options.directory:
        id3s.extend([ID3(os.path.join(options.directory, fn)) for fn in filter(lambda x: x.endswith(".mp3"), os.listdir(options.directory))])
    if options.filename:
        id3s.append(ID3(options.filename))

    for id3 in id3s:
        AmazonSource().generate_and_save(id3, options.update, options.yes)
