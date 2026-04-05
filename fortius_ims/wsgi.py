"""
WSGI config for fortius_ims project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fortius_ims.settings')
application = get_wsgi_application()
