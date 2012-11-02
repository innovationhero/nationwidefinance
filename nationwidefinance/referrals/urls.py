from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('nationwidefinance.referrals.views',
	url(r'^$', 'home', name='home'),
	url(r'^logout/$', 'logout', name='logout_user'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^check_user_profile/$', 'check_user_profile', name='check_user_profile'),
	url(r'^create_profile/$', 'create_profile', name='create_profile'),
	url(r'^add_referral/$', 'add_referral', name='add_referral'),
	#url(r'^add_referred/(?P<user_id>\d+)/$', 'add_referred', name='add_referred'),
	url(r'^sign_up/$', 'sign_up',name='sign_up'),
	
)
