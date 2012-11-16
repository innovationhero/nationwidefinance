from django.contrib.auth.models import User
from django.db import models

class Country(models.Model):

	name = models.CharField(max_length=100)
	code = models.CharField(max_length=3)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Countries"

class Industry(models.Model):

	name = models.CharField(max_length=100)
	description = models.CharField(max_length=1000)
	entity_active = models.BooleanField()

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Industries"

class EntityContact(models.Model):

	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	phone = models.CharField(max_length=100)

	def __unicode__(self):
		return '%s %s' % (self.first_name, self.last_name)

	class Meta:
		verbose_name_plural = "Entity Contacts"

class EntityReferral(models.Model):
	
	referrer = models.ForeignKey(User, related_name='referrer')
	referred = models.ManyToManyField(User, related_name='referred')
	created_date = models.DateTimeField()
	updated_date = models.DateTimeField()
	entity_active = models.BooleanField()

	def __unicode__(self):
		return '%s referred %s' % (
			self.referrer.org_name if self.referrer.entity_type == 'org' else self.referrer.first_name + ' ' + self.referrer.last_name,
			' and '.join(entity['org_name'] if entity['entity_type'] == 'org' else entity['first_name'] + ' ' + entity['last_name'] for entity in self.referred.values()))

	class Meta:
		verbose_name_plural = "Entity Referrals"

class ReferrerPoints(models.Model):

	referrer = models.ForeignKey(User, null=False, blank=False)
	value = models.IntegerField()
	entity_active = models.BooleanField()

	def __unicode__(self):
		return '%s has %d points' % (self.referrer.org_name if self.referrer.entity_type == 'org' else self.referrer.first_name + ' ' + self.referrer.last_name,
			self.value)

	class Meta:
		verbose_name_plural = "Referral Points"

class EntityPlan(models.Model):
	plan_name = models.CharField(max_length=100)
	plan_description = models.CharField(max_length=2000)
	max_referrals_allowed = models.IntegerField(null=True, blank=True)
	unlimited_referrals = models.BooleanField()
	can_add_entity = models.BooleanField()
	can_use_social_media = models.BooleanField()
	entity_active = models.BooleanField()

	def __unicode__(self):
		return self.plan_name

	class Meta:
		verbose_name_plural = "Entity Plans"

class EntityProfile(models.Model):
	
	user = models.ForeignKey(User,null=False, blank=False)
	plan = models.ForeignKey(EntityPlan, blank=True, null=True)
	industry = models.ForeignKey(Industry, null=True, blank=True)
	entity_contact = models.ForeignKey(EntityContact)

	referrals_made = models.IntegerField(null=True, blank=True)
	entity_type = models.CharField(max_length=10)
	
	business_name = models.CharField(max_length=100, null=True, blank=True)
	
	num_referrals_for_gift = models.IntegerField(null=False)
	direct_referal_value = models.FloatField(null=True, blank=True)
	indirect_reverral_value = models.FloatField(null=True, blank=True)

	address1 = models.CharField(max_length=100)
	address2 = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	province = models.CharField(max_length=100)
	country = models.ForeignKey(Country,blank=False,null=False)

	dob = models.DateTimeField(null=True, blank=True)

	created_date = models.DateTimeField()
	updated_date = models.DateTimeField()
	entity_active = models.BooleanField()


	def __unicode__(self):
		if self.entity_type == 'org':
			return self.business_name
		return '%s %s' % (self.entity_contact.first_name, self.entity_contact.last_name)

	class Meta:
		verbose_name_plural = "Entity Profiles"
