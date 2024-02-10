import os 
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

#! PROJECT SECRET-KEY
SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []

# !PROJECT APP'S
PROJECT_APPS=[
    'ecommerce',
    'authentication',
    'user_activity_logs',
]

# !THIRD PARTY APP'S 
THIRD_PARTY_APPS=[
    "debug_toolbar",
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',
]

# !INSTALLED APP'S
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

INSTALLED_APPS+=PROJECT_APPS
INSTALLED_APPS+=THIRD_PARTY_APPS

# !DJANGO DEBUG TOOLBAR CONFIGURATION'S
INTERNAL_IPS = [
    "127.0.0.1",
]



# !PROJECT MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',# !CORS Middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",# !Debug Toolbar Middleware
]

ROOT_URLCONF = 'main.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# !DEFAULT DATABASE CONFIGURATION'S 
"""
If You dont want to use postgres as your database 
You can use this instead just uncomment this one 
and comment or remove the one beneth it 
"""
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# !DATABASE CONFIGURATION'S FOR POSTGRE'S
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':os.environ.get("DB_NAME"),
        'USER': 'postgres', 
        'PASSWORD':os.environ.get("DB_PASS"), 
        'HOST': 'localhost', 

    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# !CONFIGURATION'S FOR STATIC FILES
STATIC_URL = 'static/'
STATIC_ROOT=os.path.join(BASE_DIR,'static')



# !CONFIGURATION'S FOR MEDIA FILES
MEDIA_URL='media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# !CUSTOM USER CONFIGURATION'S
AUTH_USER_MODEL='authentication.User'



# ! SIMPLE JWT CONFIGURATION'S
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}



# ! SIMPLE JWT CONFIGURATION'S
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT'),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=60),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}



# !CELERY CONFIGURATION'S
CELERY_BROKER_URL='redis://127.0.0.1:6379/0'



#! EMAIL CONFIGURATION'S
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER =os.environ.get('EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL')


# ! SUPPLIER EMAIL
SUPPLIER_EMAIL=os.environ.get('THE_SUPPLIER_EMAIL')


# ! CORS ALLOWED ORGIN FOR ALL 
CORS_ALLOW_ALL_ORIGINS = True


# ! CORS ALLOWED ORIGINS FOR SPECIFIED ORIGINS
""" 
uncomment and add origins if you want to allows only
some orgins to be allowed for CORS
"""
#* CORS_ALLOWED_ORIGINS = [
    # ! Example origins
    #? "http://localhost:8080",
    #? "http://127.0.0.1:9000"
#* ]
