from settings_local import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'nationwide',                      # Or path to database file if using sqlite3.
        'USER': 'nationwide',                      # Not used with sqlite3.
        'PASSWORD': 'Nation!23Wide',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

STATIC_ROOT = '/home/admin/nationwidefinance/nationwidefinance/static'

FACEBOOK_APP_ID                   = '361510763943252'
FACEBOOK_API_SECRET               = '2f02398f50a91ac1aea21676a098c53b'
FACEBOOK_EXTENDED_PERMISSIONS     = ['email', 'publish_stream']

TWITTER_CONSUMER_KEY              = 'brWqfOYENR4q5VMGSTw'
TWITTER_CONSUMER_SECRET           = 'eVqv0sxKta5bgbitKAGpiBnm9XCLGS0mCJSggB3GYJI'

ACCOUNT_ACTIVATION_DAYS = 7

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'info@webiken.net'
EMAIL_HOST_PASSWORD = 'Web12Iken'
EMAIL_USE_TLS = True