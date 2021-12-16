from os import environ
from django.core.wsgi import get_wsgi_application

environ.setdefault("DJANGO_SETTINGS_MODULE", "plerk.service.transaction.stats.conf")

application = get_wsgi_application()
