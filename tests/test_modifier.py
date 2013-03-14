import unittest

from pykss.modifier import Modifier


class ModiferTestCase(unittest.TestCase):

    def setUp(self):
        self.modifier = Modifier('.callout.extreme:hover', 'calls things out')

    def test_handles_pseudo(self):
        self.assertTrue('pseudo-class-hover' in self.modifier.class_name)

    def test_handles_multiple_classes(self):
        self.assertTrue('callout extreme' in self.modifier.class_name)

    def test_add_example(self):
        example = '<i class="icon$modifier_class"></i>'
        expected = '<i class="icon callout extreme pseudo-class-hover"></i>'

        self.modifier.add_example(example)
        self.assertEqual(self.modifier.example, expected)
