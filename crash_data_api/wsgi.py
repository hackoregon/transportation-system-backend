"""
WSGI config for crash_data_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

if os.environ.get('DEBUG') != "True":
    from gevent import monkey
    monkey.patch_all()

    from psycogreen.gevent import patch_psycopg
    patch_psycopg()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crash_data_api.settings")

application = get_wsgi_application()
