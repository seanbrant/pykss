from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.html import escape


register = template.Library()


class StyleguideBlockNode(template.Node):

    def __init__(self, styleguide, reference, template_name, nodelist):
        self.styleguide = styleguide
        self.reference = reference
        self.template_name = template_name
        self.nodelist = nodelist

    def __repr__(self):
        return '<StyleguideBlockNode>'

    def render(self, context):
        styleguide = self.styleguide.resolve(context)
        reference = self.reference.resolve(context)
        template_name = self.template_name.resolve(context)

        try:
            section = styleguide.section(reference)
        except Exception as e:
            if settings.TEMPLATE_DEBUG:
                raise e
            return ''

        example_html = self.nodelist.render(context).strip()

        modifier_examples = []
        for modifier in section.modifiers:
            context.update({'modifier': modifier})
            html = self.nodelist.render(context).strip()
            modifier_examples.append({
                'modifier': modifier,
                'html': mark_safe(html),
            })

        output = render_to_string(template_name, {
            'section': section,
            'example_html': mark_safe(example_html),
            'modifier_examples': modifier_examples,
            "escaped_html": escape(example_html),
        })

        return output


@register.tag
def styleguideblock(parser, token):
    """
    {% styleguideblock styleguide "1.1" %}
        <button class="{{ modifier.class_name }}">Example Button</button>
    {% endstyleguideblock %}

    {% styleguideblock styleguide "1.1" using "custom.html" %}
        <button class="{{ modifier.class_name }}">Example Button</button>
    {% endstyleguideblock %}

    """
    bits = token.split_contents()[1:]

    if len(bits) < 2:
        raise template.TemplateSyntaxError("styleguideblock expected at "
            "least two arguments")

    elif len(bits) == 2:
        styleguide, reference = bits
        template_name = '"pykss/styleguideblock.html"'

    elif len(bits) >= 3 and bits[2] != 'using':
        raise template.TemplateSyntaxError("styleguideblock expected using "
            "as the third argument")

    elif len(bits) == 3:
        raise template.TemplateSyntaxError("styleguideblock expects a "
            "template name after 'using'")

    else:
        styleguide, reference, _using, template_name = bits

    nodelist = parser.parse(('endstyleguideblock',))
    parser.delete_first_token()

    return StyleguideBlockNode(
        styleguide=parser.compile_filter(styleguide),
        reference=parser.compile_filter(reference),
        template_name=parser.compile_filter(template_name),
        nodelist=nodelist,
    )
