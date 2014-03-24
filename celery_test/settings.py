# Django settings for celery_test project.

import os

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."),
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

APPEND_SLASH = False

MANAGERS = ADMINS

TWITTER_CONSUMER_KEY = 'NvIRx26RzQ28JDZNtcuA'
TWITTER_CONSUMER_SECRET = 'ELDww8jTvIA5NV9ztFeau55m8AhV9C9iFF7fnWOFD9Q'
TWITTER_ACCESS_TOKEN_KEY = '2278792177-AxbdKG4xlFyThPkghFYJF9y4yG1SfAJ8dJ6B9PE'
TWITTER_ACCESS_TOKEN_SECRET = 'p2qCKJQTqgZJrLY6CYndmKSoambILsDhcXJ1wICqVcct1'

import djcelery
djcelery.setup_loader()


CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_ALWAYS_EAGER = False
BROKER_BACKEND = "djkombu.transport.DatabaseTransport"
CELERY_RESULT_BACKEND = 'djcelery.backends.database.DatabaseBackend'

#BROKER_URL = 'amqp://walrus:0108@localhost:5672//'
# BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Europe/Kiev'
# CELERY_IMPORTS = ("tasks",)

FACEBOOK_APP_ID = '1476093182617620'
FACEBOOK_APP_SECRET = 'e860b4c7ce963989c6f6c5817f8ce455'


DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Or path to database file if using sqlite3.
        'NAME': 'celery_test',
        # The following settings are not used with sqlite3:
        'USER': 'django',
        'PASSWORD': '0108',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
        # 'OPTIONS': {
        #     "init_command": "SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;"
        # }
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Kiev'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will memoryviewake some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
#USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.normpath(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')),
    # os.path.join(PROJECT_ROOT, "statis"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    #'djangobower.finders.BowerFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'hku+td+=xm=!0d%(9=14cxyv6d+vv6kdtqccn!cqmo%9bei+ej'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)

ROOT_URLCONF = 'celery_test.urls'

# Python dotted path to the WSGI application used by Django's runserver.
#WSGI_APPLICATION = 'ws4redis.django_runserver.application'


# ANGULAR_TEMPLATES_DIR = os.path.join(STATICFILES_DIRS[0], 'js/app/views')

# ANGULAR_TEMPLATE_TEXT = 'html'

# ANGULAR_TEMPLATE_EXCLUDE = ['list.html']


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_ROOT, 'components')

INSTALLED_APPS = (
    # 'admin_tools',
    # 'admin_tools.theming',
    # 'admin_tools.menu',
    # 'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'djcelery',
    'djkombu',
    'south',
    'rest_framework',
    'rest_framework.authtoken',
    'celery_test',
    'djangular',
    'django_nose',
    'tweets',
    'crispy_forms',
    'floppyforms',
    'compressor',
    # 'social.apps.django_app.default',
    # 'corsheaders',
)

REDIS_SSEQUEUE_CONNECTION_SETTINGS = {
    'location': 'localhost:6379',
    'db': 0,
}

# BOWER_INSTALLED_APPS = (
#     'angular',
#     'angular-resource',
#     'underscore',
#     'bootstrap',
# )

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# SESSION_ENGINE = 'redis_sessions.session'

# SOCKJS_CLASSES = (
#     'tweets.pollserver.PollConnection',
# )

CRISPY_TEMPLATE_PACK = 'bootstrap3'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',

    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


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
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend'
)

ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True

# SOCIAL_AUTH_PIPELINE = (
#     'social.pipeline.social_auth.social_details',
#     'social.pipeline.social_auth.social_uid',
#     'social.pipeline.social_auth.auth_allowed',
#     'social.pipeline.social_auth.social_user',
#     'social.pipeline.user.get_username',
#     'social.pipeline.social_auth.associate_by_email',
#     'social.pipeline.user.create_user',
#     'social.pipeline.social_auth.associate_user',
#     'social.pipeline.social_auth.load_extra_data',
#     'social.pipeline.user.user_details'
# )


# CORS_ORIGIN_ALLOW_ALL = True
#CORS_URLS_REGEX = r'^/api/.*$'
# CORS_ALLOW_HEADERS = (
#        'x-requested-with',
#        'content-type',
#        'accept',
#        'origin',
#        'authorization',
#        'x-csrftoken',
#        'x-token'
#    )

# SOCIAL_AUTH_FACEBOOK_KEY = '1476093182617620'
# SOCIAL_AUTH_FACEBOOK_SECRET = 'e860b4c7ce963989c6f6c5817f8ce455'
# SOCIAL_AUTH_FACEBOOK_SCOPE = [
#     'email', 'user_about_me', 'user_birthday', 'user_location']
