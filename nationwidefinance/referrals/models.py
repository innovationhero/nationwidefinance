from django.contrib.auth.models import User
from django.db import models

class Country(models.Model):

	name = models.CharField(max_length=100)
	code = models.CharField(max_length=3)

class Entity(User):
	
	created_date = models.DateTimeField()
	updated_date = models.DateTimeField()
	entity_active = models.BooleanField()



class Organization(Entity):
	
	entity = models.ForeignKey(Entity,related_name='org_entity')
	name = models.CharField(max_length=100)


class Person(Entity):
	
	entity = models.ForeignKey(Entity,related_name='person_entity')
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	dob = models.DateField()



class EntityReferral(models.Model):
	
	users = models.ManyToManyField(Entity, related_name='u+')
	referents = models.ManyToManyField(Entity, related_name='ref+')
	created_date = models.DateTimeField()
	updated_date = models.DateTimeField()
	entity_active = models.BooleanField()

class ReferalValue(models.Model):

	referal = models.ForeignKey(EntityReferral,null=False,blank=False)
	code = models.CharField(max_length=10)
	description = models.CharField(max_length=200)
	value = models.FloatField()
	entity_active = models.BooleanField()

class EntityProfile(models.Model):

	address1 = models.CharField(max_length=100)
	address2 = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	provide = models.CharField(max_length=100)
	county = models.ForeignKey(Country,blank=False,null=False)
