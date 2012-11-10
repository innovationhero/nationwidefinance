from django.template.loader import get_template
from django.template import Context

from celery.task import Task

from nationwidefinance.referrals import models
from nationwidefinance.mailer import send_email

class CalculateGifts(Task):

	def get_referrers(self):
		return models.Entity.objects.filter(organization__username=self.user.username)

	def set_referral_points(self):
		self.d = dict()
		for entity in self.referrers:
			self.d[entity] = entity.referrerpoints.value

	def send_emails(self):
		self.subject = 'You Have Earned A Gift'
		for entity in self.email_list:
			t = get_template('gifts_notification_emai.html')
			c = Context(dict(name = entity.org_name if entity.entity_type == 'org' else '%s %s' % (entity.first_name, entity.last_name)))
			body = t.render(c)
			send_email(subject=subject, body=body, to_email=[entity.email,])



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
