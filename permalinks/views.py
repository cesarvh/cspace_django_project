__author__ = 'jblowe'

from django import forms
from os import path
import logging

from django.shortcuts import render
from common.appconfig import loadConfiguration, loadFields
from common import cspace # we use the config file reading function
from cspace_django_site import settings
from common.utils import doSearch, loginfo

searchConfig = cspace.getConfig(path.join(settings.BASE_PARENT_DIR, 'config'), 'search')
FIELDDEFINITIONS = searchConfig.get('search', 'FIELDDEFINITIONS')

# add in the the field definitions...
prmz = loadConfiguration('common')
prmz = loadFields(FIELDDEFINITIONS, prmz)

# Get an instance of a logger, log some startup info
logger = logging.getLogger(__name__)
logger.info('%s :: %s :: %s' % ('permalink startup', '-', '%s | %s | %s' % (prmz.SOLRSERVER, prmz.IMAGESERVER, prmz.BMAPPERSERVER)))

def get_item(request, itemid):

    searchfield = ''
    for i in prmz.FIELDS['Search']:
        if 'objectno' in i['fieldtype']:
            searchfield = i['name']
            break
    requestObject = {searchfield: itemid, 'resultsOnly': 'true'}
    form = forms.Form(requestObject)

    if form.is_valid():
        context = {'searchValues': requestObject}
        context = doSearch(context, prmz, request)

        loginfo(logger, 'results.%s' % context['displayType'], context, request)
        return render(request, 'search.html', context)
