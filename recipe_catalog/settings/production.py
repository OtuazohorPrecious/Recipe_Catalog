# Production settings
from .base import *
import dj_database_url

DEBUG = True
ALLOWED_HOSTS = ['recipe-catalog.onrender.com', 'localhost']

SECRET_KEY = os.getenv('SECRET_KEY')

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('DB_HOST'),
#         'PORT': os.getenv('DB_PORT'),
#     }
# }


# Supabase Storage configuration (production-only)
# STORAGES = {
#     "default": {  # Media files (uploads)
#         "BACKEND": "django_storage_supabase.supabase.SupabaseStorage"
#     },
#     "staticfiles": {  # Static files (CSS, JS)
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
#     }
# }

STORAGES = {
    "default": {
        "BACKEND": "recipe_catalog.storage.SupabaseStorage"  # Your custom backend path
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    }
}

SUPABASE_URL = os.getenv("SUPABASE_URL")  # Set these in Render env vars
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = "media"
# Database Configuration
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}

# Add WhiteNoise middleware
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
] + MIDDLEWARE

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')