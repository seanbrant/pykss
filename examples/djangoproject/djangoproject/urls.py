from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

from pykss.contrib.django.views import StyleguideView


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^styleguide/$', StyleguideView.as_view(template_name='styleguide.html'), name='styleguide'),
)
