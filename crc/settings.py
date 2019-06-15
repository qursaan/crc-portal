"""
Django settings for crc project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# from celery import Celery

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    # get the directory where this file is
    ROOT = os.path.dirname(__file__) or '.'
    # move one step up
    ROOT = os.path.realpath(ROOT + '/..')
    # print "qursaan",ROOT
except:
    # something is badly wrong here
    ROOT = None
    import traceback

    traceback.print_exc()

# assume we have ./static present already
# @qursaan
# HTTPROOT="/usr/share/unfold"
# the place to store local data, like e.g. the sqlite db
# @qursaan
# DATAROOT="/var/unfold"
# if not there, then we assume it's from a devel tree
# @qursaan
# if not os.path.isdir(os.path.join(HTTPROOT, "static")):
HTTPROOT = ROOT
DATAROOT = ROOT
AUTHROOT = os.path.join(HTTPROOT, "auth")

if not os.path.isdir(ROOT):
    raise Exception("Cannot find ROOT %s for unfold" % ROOT)
if not os.path.isdir(HTTPROOT):
    raise Exception("Cannot find HTTPROOT %s for unfold" % HTTPROOT)

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except:
    pass


# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!d2c&%9oqijgj8nfbjp+2m!hbyb08b36-j#tglpo*t02yh3=)b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['127.0.0.1','localhost','195.246.49.19']
####################
ADMINS = (
    # ('your_name', 'your_email@test.com'),
)

MANAGERS = ADMINS
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# ******************************************************************* #
# Mail configuration
DEFAULT_FROM_EMAIL = "root@crclab.org"  # "root@theseus.ipv6.lip6.fr"
EMAIL_HOST_PASSWORD = "food"
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
EMAIL_USE_TLS = False
SUPPORT_EMAIL = "alihussin.it@gmail.com"
# Storage settings
BASE_IMAGE_DIR = "/usr/local/share/storage/"
USER_HOME = "/home/crc-users/"
# Backend setting
BACKENDIP = "127.0.0.1"  # ""193.227.16.199"
# Federation setting
FED_PASS = 'XfedXuserXcrc'
#FED_RUN = 1  # 0-STOP 1-RUNNING
FED_PORT = 7770
# ******************************************************************* #
ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window; you may, of course, use a different value.
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# System parameters
MAX_OMF_DURATION = 8
MAX_SIM_DURATION = 24 * 7
MAX_BUK_DURATION = 24 * 7
SIM_RESERVATION = False
LAB_RESERVATION = False
# @upgraded
SITE_ID = 1
BACKEND_RUN = False
# File Browser Default Directory
# FILEBROWSER_DIRECTORY = "uploads/"
THUMBNAIL_HIGH_RESOLUTION = True
FILER_CANONICAL_URL = 'uploads/'

# TEMPLATE_LOADERS = (
# 'django.template.loaders.filesystem.Loader',
# 'django.template.loaders.app_directories.Loader',
# 'django.template.loaders.eggs.Loader',
# )

# Application definition
INSTALLED_APPS = (
    # Basics
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',  # @upgraded
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party
    #'insert_above',
    # our project
    'crc',
    # core of UI
    #'manifold',
    'unfold',
    # plugins
    'plugins',
    # views
    'ui',
    'portal',
    'lab',
    'federate',
    'howdy',
    'rest_framework',
)

# CELERY_RESULT_BACKEND=('djcelery.backends.database:DatabaseBackend',)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'auth.manifoldbackend.ManifoldBackend',
)

ROOT_URLCONF = 'crc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(HTTPROOT, "templates"),
                 os.path.join(AUTHROOT, "templates"), ],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            # 'builtins': ['insert_above.templatetags.insert_tags', ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
            'builtins': [
                'django.contrib.staticfiles.templatetags.staticfiles',  # @upgraded
                'insert_above.templatetags.insert_tags',  # @upgraded
            ],
            'loaders': [
                # insert your TEMPLATE_LOADERS here
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                # 'django.template.loaders.eggs.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'crc.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, 'crc/db.cnf'),
            #'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Cairo'  # 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(ROOT, 'media')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_ROOT = os.path.join(ROOT, 'static2')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # Thierry : we do not need to detail the contents
    # of our 'apps' since they're mentioned in INSTALLED_APPS
    os.path.join(BASE_DIR, "static"),
    # os.path.join(ROOT, "static"),
)

# Needed by PluginFinder
PLUGIN_DIR = os.path.join(BASE_DIR, 'plugins')

# ThirdPartyFinder
THIRDPARTY_DIR = os.path.join(BASE_DIR, 'third-party')

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    # Thierry : no need for this one
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'unfold.collectstatic.PluginFinder',
    'unfold.collectstatic.ThirdPartyFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        },
        # 'file': {
        #    'level': 'DEBUG',
        #    'class': 'logging.FileHandler',
        #    'filename': '/path/to/django/debug.log',
        # },
    },
    'loggers': {
        'default': {
            'handlers': ['console'],
            'level': 'INFO',
            'filters': ['require_debug_false'],
        },
        'django': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        }
    },
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        #'rest_framework.authentication.BasicAuthentication',
        #'rest_framework.authentication.SessionAuthentication',
    ]
}


BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'third-party')

BOWER_PATH = '/usr/local/bin/bower'

BOWER_INSTALLED_APPS = (
    'd3#3.5.5',
    'nvd3#1.7.1',
)
