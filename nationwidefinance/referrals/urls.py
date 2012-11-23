from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('nationwidefinance.referrals.views',
	url(r'^$', 'home', name='home'),
	url(r'^logout/$', 'logout', name='logout_user'),
	url(r'^check_user_profile/$', 'check_user_profile', name='check_user_profile'),
	url(r'^create_profile/$', 'create_profile', name='create_profile'),
	url(r'^edit_profile/$', 'edit_profile', name='edit_profile'),
	url(r'^add_referral/$', 'add_referral', name='add_referral'),
	#url(r'^add_referred/(?P<user_id>\d+)/$', 'add_referred', name='add_referred'),
	url(r'^calculate_gifts/$', 'calculate_gifts',name='calculate_gifts'),
	url(r'^calculate_gifts_check/$', 'calculate_gifts_check',name='calculate_gifts_check'),
	url(r'^first_login', 'referrer_first_login', name='referrer_first_login'),
	url(r'^view_referrers/', 'view_referrers', name='view_referrers'),
	url(r'^view_referred/', 'view_referred', name='view_referred')

	
)
