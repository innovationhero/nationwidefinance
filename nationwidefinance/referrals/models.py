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


class Person(models.Model):
	user = models.ForeignKey(User,null=False,blank=False)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	dob = models.DateField()

	def __unicode__(self):
		return '%s %s' % (self.first_name, self.last_name)



class EntityReferral(models.Model):
	
	referrer = models.ForeignKey(User,related_name='referrer')
	referred = models.ManyToManyField(User, related_name='ref+')
	referred_to = models.ForeignKey(User,related_name='referred_to')
	created_date = models.DateTimeField()
	updated_date = models.DateTimeField()
	entity_active = models.BooleanField()

class ReferralValue(models.Model):

	referal = models.ForeignKey(EntityReferral,null=False,blank=False)
	code = models.CharField(max_length=10)
	description = models.CharField(max_length=200)
	value = models.FloatField()
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
