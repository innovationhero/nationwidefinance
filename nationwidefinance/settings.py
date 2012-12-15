from nationwidefinance.settings_local import *

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

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/admin/nationwidefinance/nationwidefinance/static'

DEBUG = True

FACEBOOK_APP_ID                   = '361510763943252'
FACEBOOK_API_SECRET               = '2f02398f50a91ac1aea21676a098c53b'
FACEBOOK_EXTENDED_PERMISSIONS     = ['email', 'publish_stream']

TWITTER_CONSUMER_KEY              = 'brWqfOYENR4q5VMGSTw'
TWITTER_CONSUMER_SECRET           = 'eVqv0sxKta5bgbitKAGpiBnm9XCLGS0mCJSggB3GYJI'

ACCOUNT_ACTIVATION_DAYS = 7


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'info@webiken.net'
EMAIL_HOST_PASSWORD = 'Web12Iken'
EMAIL_USE_TLS = True

BROKER_URL = 'django://'

import socket
HOSTNAME = socket.gethostname()

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'j10$28)t^52zt++tnjwwmfm)rw6o25n529#o$bfb4x4wv3)d48'

PAYPAL_RECEIVER_EMAIL = "seller_1355087471_biz@webiken.net"

PAYPAL_BUTTON_IMAGE = "https://www.sandbox.paypal.com/en_US/i/btn/btn_subscribeCC_LG.gif"

PAYPAL_CC_IMAGE = "https://www.sandbox.paypal.com/en_US/i/scr/pixel.gif"

PAYPAL_ACTION_URL = "https://www.sandbox.paypal.com/cgi-bin/webscr"

PAYPAL_NOTIFY_URL = "http://%s:8000/referrals/nationwide_paypal_ipn" % HOSTNAME

PAYPAL_CANCEL_RETURN_URL = "http://%s:8000/referrals/nationwdide_paypal_cancel" % HOSTNAME

PAYPAL_RETURN_URL = "http://%s:8000/referrals/nationwide_paypal_return" % HOSTNAME

PAYPAL_TEST = True

PAYPAL_ITEM_NAME = "Nationwide Finance"