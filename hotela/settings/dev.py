from .base import *


DEBUG = env('DEBUG')

ALLOWED_HOSTS = ["*"]


DATABASES = {
    'default': env.db('DATABASE_URL')
}