from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

import settings

urlpatterns = patterns('',
	url(r'^%s' % (settings.SUB_SITE,), include('nationwidefinance.urls_subsite')),
	#url(r'^openid/', include('django_openid_auth.urls')),
	#url(r'^accounts/profile','nationwidefinance.referrals.views.redirect_to_home'),
    
)
