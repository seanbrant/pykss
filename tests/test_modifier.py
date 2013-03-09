import unittest

from pykss.modifier import Modifier


class ModiferTestCase(unittest.TestCase):

    def setUp(self):
        self.modifier = Modifier('.callout.extreme:hover', 'calls things out')

    def test_handles_pseudo(self):
        self.assertTrue('pseudo-class-hover' in self.modifier.class_name)

    def test_handles_multiple_classes(self):
        self.assertTrue('callout extreme' in self.modifier.class_name)
