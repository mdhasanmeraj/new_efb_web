from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', "192.168.4.5",]

# Development specific settings
# Disable whitenoise in development if you prefer Django's default static serving
# MIDDLEWARE.remove('whitenoise.middleware.WhiteNoiseMiddleware')
