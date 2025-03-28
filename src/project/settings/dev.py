from .base import *

DEBUG = True

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

ALLOWED_HOSTS = []


INTERNAL_IPS = [
    "127.0.0.1",
]
