from datetime import timedelta
import urlparse

from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import User
from django.conf import settings

from social_auth.models import UserSocialAuth

from celery.task import Task
from celery.task.schedules import crontab
from celery.decorators import periodic_task

from nationwidefinance.referrals import models
from nationwidefinance.mailer import send_email
from nationwidefinance.referrals import facebook_sdk

@periodic_task(run_every=timedelta(days=7))
def post_to_facebook():

	profiles = models.EntityProfile.objects.filter(post_to_facebook=True, entity_active=True)
	users = UserSocialAuth.objects.filter(user__email__in=[profile.user.email for profile in profiles], provider='facebook')

	for user in users:

		graph = facebook_sdk.GraphAPI(user.extra_data.get('access_token'))
		graph.extend_access_token(settings.FACEBOOK_APP_ID, settings.FACEBOOK_API_SECRET)

		attachment = dict(
				description = user.facebookpostmessage.message
			)
		if user.facebookpostmessage.link or user.facebookpostmessage.link != '':
			attachment['link'] = user.facebookpostmessage.link
	
		try:
			graph.put_wall_post(user.facebookpostmessage.message, attachment)
		except Exception, e:
			print e.message	
			pass

@periodic_task(run_every=timedelta(days=7))
def post_to_twitter():

	profiles = models.EntityProfile.objects.filter(post_to_twitter=True, entity_active=True)
	users = UserSocialAuth.objects.filter(user__email__in=[profile.user.email for profile in profiles], provider='twitter')

	for user in users:
		d = urlparse.parse_qs(user.extra_data['access_token'])
		api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY, consumer_secret=settings.TWITTER_CONSUMER_SECRET, access_token_key=d['oauth_token'][0], access_token_secret=d['oauth_token_secret'][0])
		try:
			status = api.PostUpdate('example django tweet!')
		except Exception, e:
			pass

@periodic_task(run_every=timedelta(minutes=2))
def check_organization_referral_upgrade():
	profiles = models.EntityProfile.objects.filter(entity_type='org', entity_active=True)
	for profile in profiles:
		if not profile.plan.unlimited_referrals:
			if profile.referrals_made < (profile.plan.max_referrals_allowed - settings.REFERRALS_UPGRADE):
				t = get_template('organization_plan_upgrade.html')
				c = Context(dict(referrals_made=profile.referrals_made, business_name=profile.business_name, max_referrals=profile.plan.max_referrals_allowed))
				body = t.render(c)
				send_email(subject=self.subject, body=body, to_email=[entity.email,])

class CalculateGifts(Task):

	def get_referrers(self):
		return [referral.referrer for referral in models.EntityReferral.objects.filter(organization=self.user)]

	def set_referral_points(self):
		self.d = dict()
		for referrer in self.referrers:
			try:
				self.d[referrer] = models.ReferrerPoints.objects.get(organization=self.user, referrer=referrer).value
			except:
				pass

	def send_emails(self):
		self.subject = 'You Have Earned A Gift'
		for entity in self.email_list:
			t = get_template('gifts_notification_email.html')
			c = Context(dict(org_name=self.profile.business_name, name='%s %s' % (entity.first_name, entity.last_name)))
			body = t.render(c)
			send_email(subject=self.subject, body=body, to_email=[entity.email,])



	def run(self, user=None, **kwargs):
		self.user = user
		self.profile = self.user.get_profile()
		self.email_list = []
		
		self.referrers = self.get_referrers()
		self.set_referral_points()
		
		for entity,v in self.d.items():
			if v >= self.profile.num_referrals_for_gift:
				self.email_list.append(entity)

		self.send_emails()
