# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import logging
import json
import os
import requests
from mutagen.id3 import TALB, APIC, TSRC, TDRC, TRCK, TIT2, TPE1
from dateutil.parser import parse as parse_date
import musicbrainzngs

from . import __version__ as mutagenerate_version
from .util import ignore_errors, format_rows_output
from .source import Source

logger = logging.getLogger('musicbrainz')


def score_release(recording, release):
    isrc_score = recording.get('isrc-list', []) == []
    type_score = release.get('release-group', {}).get('type') != 'Album'
    ext_score = -float(recording.get('ext:score'))
    return (isrc_score, type_score, ext_score)


class MusicBrainzSource(Source):
    def __init__(self, user, password, limit):
        musicbrainzngs.auth(user, password)
        musicbrainzngs.set_useragent('Mutagenerate', '.'.join(map(str, mutagenerate_version)), user)
        self.limit = limit

    def parse_talb(self, id3, release):
        self.pop(id3, 'TALB')
        id3.add(TALB(encoding=3, text=release['title']))

    def parse_tdrc(self, id3, release):
        if release.get('date', ''):
            try:
                date = parse_date(release['date'])
            except ValueError:
                return
            self.pop(id3, 'TDRC')
            id3.add(TDRC(encoding=3, text=str(date.year)))

    def parse_tsrc(self, id3, recording):
        if recording.get('isrc-list', []):
            self.pop(id3, 'TSRC')
            id3.add(TSRC(encoding=3, text=recording['isrc-list'][0]))

    def parse_trck(self, id3, release):
        number = release.get('medium-list', [{}])[-1].get('track-list', [{}])[0].get('number')
        if number:
            self.pop(id3, 'TRCK')
            id3.add(TRCK(encoding=3, text=number))

    @ignore_errors(Exception, logger)
    def parse_apic(self, id3, release):
        release_id = release['id']
        covers = musicbrainzngs.get_image_list(release_id)
        if covers['images']:
            data = requests.get(covers['images'][0]['thumbnails']['small']).content
            self.pop(id3, 'APIC')
            id3.add(APIC(encoding=3, mime='image/jpeg', type=3, desc=u"Cover", data=data))

    def parse_tit2(self, id3, recording):
        if 'TIT2' not in id3 or id3['TIT2'].text[0] != recording.get('title'):
            print('Override title? [Y/n]')
            i = raw_input().lower() or 'y'
            if i == 'y':
                self.pop(id3, 'TIT2')
                id3.add(TIT2(encoding=3, text=recording['title']))

    def parse_tpe1(self, id3, recording):
        if 'TPE1' not in id3 or id3['TPE1'].text[0] != recording.get('artist-credit', [{}])[0].get('artist', {}).get('name'):
            print('Override artist? [Y/n]')
            i = raw_input().lower() or 'y'
            if i == 'y':
                self.pop(id3, 'TPE1')
                id3.add(TPE1(encoding=3, text=recording.get('artist-credit', [{}])[0].get('artist', {}).get('name')))

    def display_release(self, i, recording, release):
        # print('Choice: %d isrc=%s, score=%s, type=%s, album=%s, title=%s, artist=%s, year=%s, track=%s' % (
        return (
            i,
            recording.get('isrc-list', []),
            recording.get('ext:score'),
            release.get('release-group', {}).get('type'),
            release.get('title'),
            recording.get('title'),
            recording.get('artist-credit', [{}])[0].get('artist', {}).get('name'),
            release.get('date', ''),
            release.get('medium-list', [{}])[-1].get('track-list', [{}])[0].get('number')
        )

    def _generate(self, id3, update=False):
        fn = '.'.join(os.path.basename(id3.filename).split('.')[:-1])
        artist = id3['TPE1'].text[0] if 'TPE1' in id3 else fn
        title = id3['TIT2'].text[0] if 'TIT2' in id3 else fn
        args = {'artist': artist, 'recording': title, 'limit': self.limit}
        logger.debug('Searching with args=%s' % args)
        recordings = musicbrainzngs.search_recordings(**args)
        logger.debug(json.dumps(recordings))
        releases = [(recording, release) for recording in recordings['recording-list'] for release in recording.get('release-list', [])]
        if not releases:
            logger.warning('No releases found for %(artist)s - %(title)s' % locals())
            return False
        releases = sorted(releases, key=lambda x: score_release(x[0], x[1]))
        rows = [self.display_release(len(releases) - i - 1, recording, release) for i, (recording, release) in enumerate(reversed(releases))]
        rows = [['Choice', 'ISRC', 'Type', 'Score', 'Album', 'Title', 'Artist', 'Year', 'Track']] + rows
        print(format_rows_output(rows))
        print('Your choice? ')
        i = raw_input()
        if not i.isdigit():
            logger.warning('Cannot recognize input, skipping')
            return False
        recording, release = releases[int(i)]
        self.parse_talb(id3, release)
        self.parse_tdrc(id3, release)
        self.parse_trck(id3, release)
        self.parse_tsrc(id3, recording)
        self.parse_tit2(id3, recording)
        self.parse_tpe1(id3, recording)
        self.parse_apic(id3, release)

        logger.debug(json.dumps(recording))
        return True
