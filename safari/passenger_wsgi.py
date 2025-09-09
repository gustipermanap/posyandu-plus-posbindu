# import imp
# import os
# import sys


#sys.path.insert(0, os.path.dirname(__file__))

#wsgi = imp.load_source('wsgi', 'Safari/wsgi.py')
#application = wsgi.application
import sys

sys.path.insert(0, "/home/ponm2847/pondoksafariindah.com/Safari")

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Safari.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()