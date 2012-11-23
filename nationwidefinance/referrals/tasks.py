from django.template.loader import get_template
from django.template import Context

from celery.task import Task

from nationwidefinance.referrals import models
from nationwidefinance.mailer import send_email

class CalculateGifts(Task):

	def get_referrers(self):
		return [referral.referrer for referral in models.EntityReferral.objects.filter(organization=self.user)]

	def set_referral_points(self):
		self.d = dict()
		for referrer in self.referrers:
			try:
				self.d[referrer] = referrer.referrerpoints_set.get().value
			except:
				pass

	def send_emails(self):
		self.subject = 'You Have Earned A Gift'
		for entity in self.email_list:
			t = get_template('gifts_notification_email.html')
			c = Context(dict(org_name=self.profile.organization_name, name = entity.org_name if entity.entity_type == 'org' else '%s %s' % (entity.first_name, entity.last_name)))
			body = t.render(c)
			send_email(subject=self.subject, body=body, to_email=[entity.email_address,])



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
