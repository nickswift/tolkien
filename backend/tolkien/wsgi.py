"""
WSGI config for tolkien project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys

# Get this app on the python path
pythonpath = '/django/tolkien/'
if pythonpath in sys.path:
    sys.path.append(pythonpath)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tolkien.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
