from .settings_base import *

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-w$@1286^cqdzo!+jp@w3$6kv9ngh^ckl$-ntl0%tv6_3)&u)&@')

DEBUG = 1

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    'http://example.com',
    'http://127.0.0.1:8080',
    'http://localhost:8080',
)

INTERNAL_IPS = [
    '127.0.0.1',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}