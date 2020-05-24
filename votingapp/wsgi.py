"""
WSGI config for votingapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votingapp.settings')

sys.path.append('/opt/votingapp')
sys.path.append('/opt/votingapp/votingapp')


application = get_wsgi_application()
