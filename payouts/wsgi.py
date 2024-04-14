"""
WSGI config for payouts project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os  # noqa

from dj_static import Cling  # noqa
from django.core.wsgi import get_wsgi_application  # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "payouts.settings")

application = Cling(get_wsgi_application())
