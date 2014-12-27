#!/usr/bin/python
# -*- coding: utf-8 -*-


from core import ID3, AmazonSource
from log import logging

import os
import requests_cache

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

from optparse import OptionParser

parser = OptionParser()
parser.add_option("", "--directory", dest="directory", default="", help="Directory")
parser.add_option("", "--filename", dest="filename", default="", help="filename")
parser.add_option("", "--cache", dest="cache", default="", help="cache")
options, args = parser.parse_args()


if __name__ == "__main__":
    requests_cache.install_cache(options.cache)
    id3s = []
    if options.directory:
        id3s.extend([ID3(os.path.join(options.directory, fn)) for fn in filter(lambda x: x.endswith(".mp3"), os.listdir(options.directory))])
    if options.filename:
        id3s.append(ID3(options.filename))

    for id3 in id3s:
        AmazonSource().generate_and_save(id3)
