import os
import unittest

import pykss


class ParseTestCase(unittest.TestCase):

    def setUp(self):
        fixtures = os.path.join(os.path.dirname(__file__), 'fixtures')
        self.scss = pykss.Parser(os.path.join(fixtures, 'scss'))
        self.less = pykss.Parser(os.path.join(fixtures, 'less'))
        self.sass = pykss.Parser(os.path.join(fixtures, 'sass'))
        self.css = pykss.Parser(os.path.join(fixtures, 'css'))
        self.multiple = pykss.Parser(os.path.join(fixtures, 'scss'), os.path.join(fixtures, 'less'))

    def test_parses_kss_comments_in_scss(self):
        self.assertEqual(self.scss.section('2.1.1').description, 'Your standard form button.')

    def test_parses_kss_comments_in_less(self):
        self.assertEqual(self.less.section('2.1.1').description, 'Your standard form button.')

    def test_parses_kss_multi_line_comments_in_sass(self):
        self.assertEqual(self.sass.section('2.1.1').description, 'Your standard form button.')

    def test_parses_kss_single_line_comments_in_sass(self):
        self.assertEqual(self.sass.section('2.2.1').description, 'A button suitable for giving stars to someone.')

    def test_parses_kss_comments_in_css(self):
        self.assertEqual(self.css.section('2.1.1').description, 'Your standard form button.')

    def test_parses_nested_scss_documents(self):
        self.assertEqual(self.scss.section('3.0.0').description, 'Your standard form element.')
        self.assertEqual(self.scss.section('3.0.1').description, 'Your standard text input box.')

    def test_parses_nested_less_documents(self):
        self.assertEqual(self.less.section('3.0.0').description, 'Your standard form element.')
        self.assertEqual(self.less.section('3.0.1').description, 'Your standard text input box.')

    def test_parses_nested_sass_documents(self):
        self.assertEqual(self.sass.section('3.0.0').description, 'Your standard form element.')
        self.assertEqual(self.sass.section('3.0.1').description, 'Your standard text input box.')

    def test_parse_returns_dictionary_of_sections(self):
        self.assertEqual(len(self.css.sections), 2)

    def test_parse_multiple_paths(self):
        self.assertEqual(len(self.multiple.sections), 6)
