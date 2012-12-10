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
	url(r'^view_referred/', 'view_referred', name='view_referred'),
	url(r'^add_referral_autocomplete/', 'add_referral_autocomplete', name='add_referral_autocomplete'),
	url(r'^post_to_facebook/', 'post_to_facebook', name='post_to_facebook'),
	url(r'^post_to_twitter/', 'post_to_twitter', name='post_to_twitter'),
	url(r'^search_referrers/', 'search_referrers', name='search_referrers'),
	url(r'^search_organization/', 'search_organization', name='search_organization'),
	url(r'^get_plan_price/', 'get_plan_price', name='get_plan_price'),
	url(r'^nationwide_paypal_return/', 'nationwide_paypal_return', name='nationwide_paypal_return'),
	
)
