import os
from django.core.wsgi import get_wsgi_application
from vercel_wsgi import make_handler

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "ecommerce_site.settings"
)

application = get_wsgi_application()
handler = make_handler(application)
