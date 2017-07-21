__author__ = 'jblowe'

# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from common import cspace  # we use the config file reading function
from cspace_django_site import settings

from os import path
import urllib2
import time
import logging
import base64
import re

config = cspace.getConfig(path.join(settings.BASE_PARENT_DIR, 'config'), 'imageserver')
username = config.get('connect', 'username')
password = config.get('connect', 'password')
hostname = config.get('connect', 'hostname')
realm = config.get('connect', 'realm')
protocol = config.get('connect', 'protocol')
port = config.get('connect', 'port')
port = ':%s' % port if port else ''

imageunavailable = config.get('info', 'imageunavailable')

unavailable_mime_type = 'jpg'
try:
    unavailable_mime_type = re.search(r'^.*?\.(.*)', imageunavailable).group(1)
    if unavailable_mime_type.lower() == 'svg':
        unavailable_mime_type = 'svg+xml'
except:
    print 'could not extract MIME-type for 404 image: %s; assuming "jpg"' % imageunavailable

try:
    derivatives_served = config.get('info', 'derivatives_served')
    derivatives_served = derivatives_served.split(',')
    print 'Derivatives served: %s' % derivatives_served
except:
    print 'No derivatives are restricted'
    derivatives_served = None

server = protocol + "://" + hostname + port

# Get an instance of a logger, log some startup info
logger = logging.getLogger(__name__)
logger.info('%s :: %s :: %s' % ('imageserver startup', '-', '%s' % server))

# @login_required()
def get_image(request, image):
    elapsedtime = time.time()
    try:
        # if the user is authenticated, they can see anything.
        # otherwise, they see only what the imageserver is configured to let them see.
        if not request.user.is_authenticated():
            image_ok = False
            # if no list of authorized derivatives is set in the config file, all are available
            if not derivatives_served:
                image_ok = True
            # otherwise if a list was specified, check to see if we can serve this derivative
            else:
                for derivative in derivatives_served:
                    if derivative in image:
                        image_ok = True
                        break
            if not image_ok:
                html = '''
            <div style="height: 90px; width: 96px; background-color: lightgray; font-size: 80%;">
            <br/>&nbsp;[not authorized]
            </div>'''
                return HttpResponse(html, content_type='text/html')

        passman = urllib2.HTTPPasswordMgr()
        passman.add_password(realm, server, username, password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)

        unencoded_credentials = "%s:%s" % (username, password)
        auth_value = 'Basic %s' % base64.b64encode(unencoded_credentials).strip()
        opener.addheaders = [('Authorization', auth_value)]
        urllib2.install_opener(opener)
        url = "%s/cspace-services/%s" % (server, image)
        f = urllib2.urlopen(url)

        msg = 'image'
        data = f.read()
        headers = f.info()
        content_type = headers.type
        content_disposition = ''
        for h in headers.headers:
            if 'Content-Disposition' in h:
                content_disposition = h
                break
        try:
            extractfilename = re.search('filename="(.*)"',content_disposition)
            filename = extractfilename.group(1)
        except:
            filename = ''

    except:
        msg = 'image error'
        data = open(path.join(settings.STATIC_ROOT, 'cspace_django_site/images', imageunavailable), 'r').read()
        content_type = 'image/%s' % unavailable_mime_type
        filename = imageunavailable

    elapsedtime = time.time() - elapsedtime
    logger.info('%s :: %s :: %s' % (msg, '-', '%s :: %8.3f seconds' % (image, elapsedtime)))
    response = HttpResponse(data, content_type=content_type)
    response['Content-Disposition'] = "filename=%s" % filename
    return response
