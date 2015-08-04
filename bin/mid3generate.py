#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import os
from mutagen.id3 import ID3
from mutagenerate.amazon import AmazonSource
from mutagenerate.musicbrainz import MusicBrainzSource
from mutagenerate.log import logger
from mutagenerate.util import list_directory

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--cache', dest='cache', default='', help='cache')
parser.add_argument('--update', dest='update', default=False, action='store_true', help='Update existing frames')
parser.add_argument('--yes', dest='yes', default=False, action="store_true", help='Say yes to saving')
parser.add_argument('--source', dest='sources', choices=('amazon', 'musicbrainz'), action='append', help='Comma separated list of sources')
group = parser.add_argument_group('MusicBrainz', 'Options for MusicBrainz')
group.add_argument('--musicbrainz-user', dest='musicbrainz_user', default='')
group.add_argument('--musicbrainz-password', dest='musicbrainz_password', default='')
group.add_argument('--musicbrainz-limit', dest='musicbrainz_limit', default=30, type=int)
parser.add_argument('paths', nargs='+')
args = parser.parse_args()


if __name__ == "__main__":
    if args.cache:
        try:
            import requests_cache
            requests_cache.install_cache(args.cache)
        except ImportError as e:
            logger.warning("Cannot set cache, install requests_cache first")
    id3s = []
    for path in args.paths:
        if os.path.isdir(path):
            id3s.extend(map(ID3, list_directory(path, 'mp3')))
        else:
            id3s.append(ID3(path))

    sources_dict = {
        'musicbrainz': MusicBrainzSource(
            args.musicbrainz_user,
            args.musicbrainz_password,
            args.musicbrainz_limit
        ),
        'amazon': AmazonSource()
    }
    sources = filter(bool, map(sources_dict.get, args.sources))
    for id3 in id3s:
        for source in sources:
            id3 = source.generate_and_save(id3, args.update, args.yes)
