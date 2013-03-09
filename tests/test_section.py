import unittest

from pykss.section import Section


class SectionTestCase(unittest.TestCase):

    def setUp(self):
        comment = """
# Form Button

Your standard form button.

:hover    - Highlights when hovering.
:disabled - Dims the button when disabled.
.primary  - Indicates button is the primary action.
.smaller  - A smaller button

Styleguide 2.1.1.
        """
        self.section = Section(comment.strip(), 'example.css')

    def test_parses_the_description(self):
        self.assertEqual(self.section.description, '# Form Button\n\nYour standard form button.')

    def test_parses_the_modifiers(self):
        self.assertEqual(len(self.section.modifiers), 4)

    def test_parses_modifier_names(self):
        self.assertEqual(self.section.modifiers[0].name, ':hover')

    def test_parses_modifier_descriptions(self):
        self.assertEqual(self.section.modifiers[0].description, 'Highlights when hovering.')

    def test_parses_the_styleguide_reference(self):
        self.assertEqual(self.section.section, '2.1.1')
