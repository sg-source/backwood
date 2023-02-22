from .settings_base import *

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-w$@1286^cqdzo!+jp@w3$6kv9ngh^ckl$-ntl0%tv6_3)&u)&@')

DEBUG = os.environ.get('DEBUG', 0)

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')

CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOWED_ORIGINS = [
    'https://backwood.online',
    'http://backwood.online',
    'https://192.168.1.22',
    'http://192.168.1.22',
]

CORS_ORIGIN_WHITELIST = (
    'https://backwood.online',
    'http://backwood.online',
    'https://192.168.1.22',
    'http://192.168.1.22',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}