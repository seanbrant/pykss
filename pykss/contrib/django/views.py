from django.conf import settings
from django.views.generic.base import ContextMixin, TemplateView

import pykss


class StyleguideMixin(ContextMixin):

    def get_styleguide(self):
        dirs = getattr(settings, 'PYKSS_DIRS', [])
        return pykss.Parser(*dirs)

    def get_context_data(self, **kwargs):
        context = {'styleguide': self.get_styleguide()}
        context.update(kwargs)
        return super(StyleguideMixin, self).get_context_data(**context)


class StyleguideView(StyleguideMixin, TemplateView):
    pass
