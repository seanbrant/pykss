import os

from django.conf import settings
from django.test import TestCase

from pykss.contrib.django.views import StyleguideMixin, StyleguideView


class StyleguideMixinTestCase(TestCase):

    def test_get_styleguide_get_dirs_from_settings(self):
        css = os.path.join(settings.PROJECT_ROOT, 'tests', 'fixtures', 'css')
        with self.settings(PYKSS_DIRS=[css]):
            styleguide = StyleguideMixin().get_styleguide()
            self.assertEqual(styleguide.section('2.1.1').description, 'Your standard form button.')

    def test_get_context_data_adds_sytleguide_to_context(self):
        self.assertIn('styleguide', StyleguideView().get_context_data())
