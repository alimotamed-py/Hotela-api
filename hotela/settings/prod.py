from .base import *


DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS') 

DATABASES = {
    'default': env.db('DATABASE_URL')
}


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True) 


STATIC_ROOT = BASE_DIR / 'staticfiles'