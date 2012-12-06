from django.conf.urls.defaults import *

from nationwidefinance.referrals.facebook import facebook_view

import settings

urlpatterns = patterns('',
	url(r'referrals/', include('nationwidefinance.referrals.urls')),
	url(r'', include('social_auth.urls')),
	url(r'^fb/', facebook_view, name='fb_app'),
	url(r'^accounts/', include('nationwidefinance.registration.urls')),
)