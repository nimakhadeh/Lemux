# -*- coding: utf-8 -*-
"""WSGI config"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'propanalyzer_api.settings')
application = get_wsgi_application()