from django.contrib.auth.models import User
from django.db import models

class Country(models.Model):

	name = models.CharField(max_length=100)
	code = models.CharField(max_length=3)

	def __unicode__(self):
		return self.name

class Organization(models.Model):
	user = models.ForeignKey(User,null=False,blank=False)
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

class Entity(models.Model):
	entity_type = models.CharField(max_length=10)
	org_name = models.CharField(max_length=100, null=True, blank=True)
	first_name = models.CharField(max_length=100, null=True, blank=True)
	last_name = models.CharField(max_length=100, null=True, blank=True)
	email_address = models.CharField(max_length=100, null=True, blank=True)
	dob = models.DateTimeField(null=True, blank=True)
	created_date = models.DateTimeField()
	updated_date = models.DateTimeField()
	entity_active = models.BooleanField()

	def __unicode__(self):
		if self.entity_type == 'org':
			return self.org_name
		return '%s %s' % (self.first_name, self.last_name)



class EntityReferral(models.Model):
	
	referrer = models.ForeignKey(Entity, related_name='referrer')
	referred = models.ManyToManyField(Entity, related_name='referred')
	created_date = models.DateTimeField()
	updated_date = models.DateTimeField()
	entity_active = models.BooleanField()

	def __unicode__(self):
		return '%s referred %s' % (
			self.referrer.org_name if self.referrer.entity_type == 'org' else self.referrer.first_name + ' ' + self.referrer.last_name,
			' and '.join(entity['org_name'] if entity['entity_type'] == 'org' else entity['first_name'] + ' ' + entity['last_name'] for entity in self.referred.values()))

class ReferrerPoints(models.Model):

	referrer = models.ForeignKey(Entity, null=False, blank=False)
	value = models.IntegerField()
	entity_active = models.BooleanField()

class EntityProfile(models.Model):
	user = models.ForeignKey(User,null=False,blank=False)
	address1 = models.CharField(max_length=100)
	address2 = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	province = models.CharField(max_length=100)
	country = models.ForeignKey(Country,blank=False,null=False)

	def __unicode__(self):
		return '%s -- %s -- %s' % (self.address1, self.city, self.province)
