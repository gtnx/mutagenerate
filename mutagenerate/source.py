# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import logging
from .util import query_yes_no

logger = logging.getLogger('mutagenerate')


class Source(object):
    def generate(self, id3, update=False):
        logger.info('Generating sources for %s' % id3.pprint().replace('\n', ', '))
        retval = self._generate(id3, update)
        logger.info('Generated sources for %s' % id3.pprint().replace('\n', ', '))
        return retval

    def generate_and_save(self, id3, update=False, yes=False):
        if self.generate(id3, update) and (yes or query_yes_no("Confirm saving ?")):
            id3.save()
        return id3

    def pop(self, id3, frame):
        if frame in id3:
            id3.pop(frame)
