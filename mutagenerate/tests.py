# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import unittest

from .util import format_rows_output


class UtilTestCase(unittest.TestCase):
    def test_format_rows_output(self):
        self.assertEqual(format_rows_output([]), '')
        self.assertEqual(format_rows_output([[]]), '')
        self.assertEqual(format_rows_output([[], []]), '\n')
        self.assertEqual(format_rows_output([['a']]), 'a')
        self.assertEqual(format_rows_output([[u'é']]), u'é')
        self.assertEqual(format_rows_output([[u'é'], ['ab']]), u' é\nab')
