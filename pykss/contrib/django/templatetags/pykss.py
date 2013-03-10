from django import template
from django.template.loader import render_to_string


register = template.Library()


class StyleGuideBlockNode(template.Node):

    def __init__(self, styleguide, reference, template_name, nodelist):
        self.styleguide = styleguide
        self.reference = reference
        self.template_name = template_name
        self.nodelist = nodelist

    def __repr__(self):
        return '<StyleGuideBlockNode>'

    def render(self, context):
        styleguide = self.styleguide.resolve(context)
        reference = self.reference.resolve(context)
        template_name = self.template_name.resolve(context)

        section = styleguide.section(reference)

        example_html = self.nodelist.render(context)

        modifier_examples = []
        for modifier in section.modifiers:
            context.update({'modifier': modifier})
            modifier_examples.append({
                'modifier': modifier,
                'html': self.nodelist.render(context),
            })

        output = render_to_string(template_name, {
            'section': section,
            'example_html': example_html,
            'modifier_examples': modifier_examples,
        })

        return output


@register.tag
def styleguideblock(parser, token):
    bits = token.contents.split()

    if len(bits) != 3:
        raise template.TemplateSyntaxError("styleguideblock expected at least two arguments")

    try:
        tag, styleguide, reference, template_name = bits
    except ValueError:
        tag, styleguide, reference = bits
        template_name = '"pykss/styleguideblock.html"'

    nodelist = parser.parse(('endstyleguideblock',))
    parser.delete_first_token()

    return StyleGuideBlockNode(
        styleguide=parser.compile_filter(styleguide),
        reference=parser.compile_filter(reference),
        template_name=parser.compile_filter(template_name),
        nodelist=nodelist,
    )
