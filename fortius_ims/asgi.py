"""
ASGI config for fortius_ims project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fortius_ims.settings')
application = get_asgi_application()
