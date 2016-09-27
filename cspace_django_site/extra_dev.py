# settings needed for Development

# get the tracking id for dev
from trackingids import trackingids

UA_TRACKING_ID = trackingids['webapps-dev'][0]

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'rest_framework',
    'django_tables2',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # 'demo' apps -- uncomment for debugging or demo
    'hello',
    'service',
    # 'service' apps: no UI
    'common',
    'suggest',
    'suggestpostgres',
    'suggestsolr',
    #'batchuploadimages',
    # 'standard' apps
    #'asura',
    #'adhocreports',
    'imagebrowser',
    'imageserver',
    'imaginator',
    'internal',
    'ireports',
    'landing',
    'search',
    #'taxonomyeditor',
    #'toolbox',
    #'simplesearch',
    'uploadmedia',
    #'uploadtricoder',
)
