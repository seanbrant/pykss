from django.conf import settings
from django.views.generic.base import TemplateView

import pykss


class StyleguideMixin(object):

    def get_styleguide(self):
        dirs = getattr(settings, 'PYKSS_DIRS', [])
        return pykss.Parser(*dirs)

    def get_context_data(self, **kwargs):
        context = super(StyleguideMixin, self).get_context_data(**kwargs)
        context.update({'styleguide': self.get_styleguide()})
        return context


class StyleguideView(StyleguideMixin, TemplateView):
    pass
