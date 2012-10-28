from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('nationwidefinance.referrals.views',
	url(r'^$', 'home', name='home'),
	url(r'^logout/$', 'logout', name='logout_user'),
	url(r'^openid_login/(?P<provider>\w+)$', 'openid_login', name='openid_login'),
	
)
