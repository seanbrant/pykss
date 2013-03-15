import os

from django.conf import settings
from django.template import Context, Template, TemplateSyntaxError
from django.test import TestCase
from django.utils import simplejson

from mock import patch, ANY

from pykss.parser import Parser


class StyleguideBlockTestCase(TestCase):

    def setUp(self):
        css = os.path.join(settings.PROJECT_ROOT, 'tests', 'fixtures', 'css')
        self.styleguide = Parser(css)

    def test_when_section_does_not_exist(self):
        template = Template("""
            {% load pykss %}
            {% styleguideblock styleguide "99" %}
            {% endstyleguideblock %}
        """)
        context = Context({'styleguide': self.styleguide})
        self.assertEquals(template.render(context).strip(), '')

    @patch('pykss.contrib.django.templatetags.pykss.render_to_string')
    def test_uses_default_template(self, mock_render_to_string):
        mock_render_to_string.return_value = ''
        template = Template("""
            {% load pykss %}
            {% styleguideblock styleguide "2.1.1" %}
            {% endstyleguideblock %}
        """)
        context = Context({'styleguide': self.styleguide})
        template.render(context)
        mock_render_to_string.assert_called_with('pykss/styleguideblock.html', ANY)

    @patch('pykss.contrib.django.templatetags.pykss.render_to_string')
    def test_allows_overiding_template(self, mock_render_to_string):
        mock_render_to_string.return_value = ''
        template = Template("""
            {% load pykss %}
            {% styleguideblock styleguide "2.1.1" using "custom.html" %}
            {% endstyleguideblock %}
        """)
        context = Context({'styleguide': self.styleguide})
        template.render(context)
        mock_render_to_string.assert_called_with('custom.html', ANY)

    def test_when_using_argument_is_wrong(self):
        text = """
            {% load pykss %}
            {% styleguideblock styleguide "2.1.1" "custom.html" %}
            {% endstyleguideblock %}
        """
        self.assertRaises(TemplateSyntaxError, Template, text)

    def test_when_using_is_defined_without_template(self):
        text = """
            {% load pykss %}
            {% styleguideblock styleguide "2.1.1" using %}
            {% endstyleguideblock %}
        """
        self.assertRaises(TemplateSyntaxError, Template, text)

    def test_renders_correctly(self):
        template = Template("""
            {% load pykss %}
            {% styleguideblock styleguide "2.1.1" using "django.html" %}
                <i class="main$modifier_class"></i>
            {% endstyleguideblock %}
        """)
        context = Context({'styleguide': self.styleguide})
        results = simplejson.loads(template.render(context))
        self.assertEqual(results['section'], '2.1.1')
        self.assertEqual(results['filename'], 'buttons.css')
        self.assertEqual(results['description'], 'Your standard form button.')
        self.assertEqual(results['modifiers'][0], [':hover', 'Highlights when hovering.'])
        self.assertEqual(results['example_html'], '<i class="main"></i>')
        self.assertEqual(results['modifier_examples'][0], [':hover', '<i class="main pseudo-class-hover"></i>'])


#class RenderStyleguideTestCase(TestCase):

#    def test_renders_correctly(self):
