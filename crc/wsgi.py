"""
WSGI config for crc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

if __name__ == '__main__':
    import django
    django.setup()


import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'crc.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crc.settings")

#from django.core.management import setup_environ
#from crc import settings
#setup_environ(settings)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()