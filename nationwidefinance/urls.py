from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.http import HttpResponseRedirect


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from referrals.facebook import facebook_view

urlpatterns = patterns('',
	url(r'^$', include('nationwidefinance.referrals.urls')),
	url(r'referrals/', include('nationwidefinance.referrals.urls')),
	url(r'', include('social_auth.urls')),
	url(r'^fb/', facebook_view, name='fb_app'),
	url(r'^accounts/', include('nationwidefinance.registration.urls')),
	url(r'^admin/', include(admin.site.urls)),
	#url(r'^openid/', include('django_openid_auth.urls')),
	#url(r'^accounts/profile','nationwidefinance.referrals.views.redirect_to_home'),
    
)
