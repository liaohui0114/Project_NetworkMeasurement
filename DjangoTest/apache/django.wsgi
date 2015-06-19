import os
import sys
#import django.core.handlers.wsgi

path = '/home/liaohui/workspace/DjangoTest'
if path not in sys.path:
    sys.path.insert(0, '/home/liaohui/workspace/DjangoTest')
os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoTest.settings'

#application = django.core.handlers.wsgi.WSGIHandler()

########copy from wsgi.py in Django####
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
#######end! it's important########

