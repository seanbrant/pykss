from django import template
from django.template.loader import render_to_string


register = template.Library()


class BaseStyleguideNode(template.Node):

    def __init__(self, styleguide, reference, template_name, nodelist):
        self.styleguide = styleguide
        self.reference = reference
        self.template_name = template_name
        self.nodelist = nodelist

    def __repr__(self):
        return '<StyleguideBlockNode>'

    @classmethod
    def as_tag(cls, parser, token):
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

        return cls.dispatch(parser, styleguide, reference, template_name)

    @classmethod
    def dispatch(cls, parser, styleguide, reference, template_name):
        raise NotImplementedError

    def render(self, context):
        styleguide = self.styleguide.resolve(context)
        reference = self.reference.resolve(context)
        template_name = self.template_name.resolve(context)

        sections = sorted([sec for ref, sec in styleguide.sections.iteritems()
                    if ref.startswith(reference)], key=lambda s: s.section)

        if self.nodelist:
            example = self.nodelist.render(context).strip()
            for section in sections:
                section.add_example(example)

        output = []

        for section in sections:
            context.update({'section': section})
            html = render_to_string(template_name, context)
            output.append(html)
            context.pop()

        return ''.join(output)


class StyleguideBlockNode(BaseStyleguideNode):

    @classmethod
    def dispatch(cls, parser, styleguide, reference, template_name):
        nodelist = parser.parse(('endstyleguideblock',))
        parser.delete_first_token()
        return cls(
            styleguide=parser.compile_filter(styleguide),
            reference=parser.compile_filter(reference),
            template_name=parser.compile_filter(template_name),
            nodelist=nodelist,
        )


class RenderStyleguideNode(BaseStyleguideNode):

    @classmethod
    def dispatch(cls, parser, styleguide, reference, template_name):
        return cls(
            styleguide=parser.compile_filter(styleguide),
            reference=parser.compile_filter(reference),
            template_name=parser.compile_filter(template_name),
            nodelist=None,
        )


@register.tag
def styleguideblock(parser, token):
    """
    {% styleguideblock styleguide "1.1" %}
        <button class="$modifier_class">Example Button</button>
    {% endstyleguideblock %}

    {% styleguideblock styleguide "1.1" using "custom.html" %}
        <button class="$modifier_class">Example Button</button>
    {% endstyleguideblock %}

    """
    return StyleguideBlockNode.as_tag(parser, token)


@register.tag
def renderstyleguide(parser, token):
    """
    {% renderstyleguide styleguide "1.1" %}

    {% renderstyleguide styleguide "1.1" using "custom.html" %}
    """
    return RenderStyleguideNode.as_tag(parser, token)
