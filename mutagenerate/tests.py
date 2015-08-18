# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import unittest

import mutagenerate.util as util


class UtilTestCase(unittest.TestCase):
    def test_format_rows_output(self):
        self.assertEqual(util.format_rows_output([]), '')
        self.assertEqual(util.format_rows_output([[]]), '')
        self.assertEqual(util.format_rows_output([[], []]), '\n')
        self.assertEqual(util.format_rows_output([['a']]), 'a')
        self.assertEqual(util.format_rows_output([[u'é']]), u'é')
        self.assertEqual(util.format_rows_output([[u'é'], ['ab']]), u' é\nab')

    def test_int_or_self(self):
        self.assertEqual(None, util.int_or_self(None))
        self.assertEqual('', util.int_or_self(''))
        self.assertEqual(1, util.int_or_self('1'))
        self.assertEqual('a', util.int_or_self('a'))
        self.assertEqual('1a', util.int_or_self('1a'))

    def test_query_yes_no(self):
        def return_yes():
            return 'yes'

        def return_empty():
            return ''
        util.raw_input = return_yes
        self.assertTrue(util.query_yes_no(''))
        self.assertTrue(util.query_yes_no('', None))
        self.assertTrue(util.query_yes_no('', 'no'))
        util.raw_input = return_empty
        self.assertTrue(util.query_yes_no('', 'yes'))

    def test_print_length(self):
        self.assertEqual(util.print_length(0), '00:00')
        self.assertEqual(util.print_length(1), '00:01')
        self.assertEqual(util.print_length(60), '01:00')
        self.assertEqual(util.print_length(305), '05:05')
