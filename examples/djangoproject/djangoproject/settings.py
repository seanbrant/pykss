import os

PROJECT_ROOT = os.path.dirname(__file__)

DEBUG = True
SECRET_KEY = 'G0GS4C7QLq3FhdDYrNtDuEBoLuXzDqaS'
ROOT_URLCONF = 'djangoproject.urls'

TEMPLATE_DIRS = [os.path.join(PROJECT_ROOT, 'templates')]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public')

STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, 'static')]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

PYKSS_DIRS = [os.path.join(PROJECT_ROOT, 'static', 'css')]

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'pykss.contrib.django',
]
