from datetime import datetime 

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from nationwidefinance.referrals import models

class CreateEntity(forms.ModelForm):

	entity_type = forms.ChoiceField(required=True, widget=forms.Select, choices=[('', u'Select'), ('org', 'Organization'), ('person', 'Person')])
	org_name = forms.CharField(required=False)
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)
	email_address = forms.CharField(required=True)
	dob = forms.DateTimeField(required=False)

	def clean_org_name(self):
		if self.cleaned_data.get('entity_type')  \
			and self.cleaned_data['entity_type'] == 'org' \
			and not self.cleaned_data.get('org_name'):
				raise forms.ValidationError('Organization name required')
		return self.cleaned_data['org_name']

	def clean_first_name(self):
		if self.cleaned_data.get('entity_type') \
			and self.cleaned_data['entity_type'] == 'person' \
			and not self.cleaned_data.get('first_name'):
				raise forms.ValidationError('First name required')
		return self.cleaned_data['first_name']

	def clean_last_name(self):
		if self.cleaned_data.get('entity_type') \
			and self.cleaned_data['entity_type'] == 'person' \
			and not self.cleaned_data['last_name']:
				raise forms.ValidationError('Last name required')
		return self.cleaned_data['last_name']	

	def clean_dob(self):
		if self.cleaned_data.get('entity_type') \
			and self.cleaned_data['entity_type'] == 'person' \
			and not self.cleaned_data.get('dob'):
				raise forms.ValidationError('DOB required')
		return self.cleaned_data['dob']	

	def save(self):
		try:
			entity = models.Entity.objects.get(email_address=self.cleaned_data['email_address'])
			return entity
		except models.Entity.DoesNotExist, e:
			entity = super(CreateEntity,self).save(commit=False)
			entity.entity_active = True
			entity.updated_date = datetime.now()
			entity.created_date = datetime.now()
			entity.save()
			return entity


	class Meta:
		model = models.Entity
		exclude = ('entity_active', 'created_date', 'updated_date',)

class CreateReferralForm(forms.Form):

	referred = forms.IntegerField()
	referrer = forms.MultipleChoiceField()

	def save(self):
		refferer_entity = models.Entity.objects.get(pk=referrer)
		referral.entity_active = True
		referral.created_date = datetime.now()
		referral.updated_date = datetime.now()
		referral.save()
		super(CreateReferral, self).save_m2m()
		return referral

## It appears one form class can be used for creating a profile and signing up
class CreateProfileForm(forms.ModelForm):

	name = forms.CharField(required=False)
	address2 = forms.CharField(required=False)
	country = forms.ModelChoiceField(queryset=models.Country.objects.all(), empty_label="Select...")

	def __init__(self,user=None,*args,**kwargs):
		self.user = user
		super(CreateProfileForm,self).__init__(*args,**kwargs)

	def save(self):
		profile = super(CreateProfileForm,self).save(commit=False)
		profile.user = self.user
		profile.save()
		org = models.Organization()
		org.name = self.cleaned_data.get('name')
		org.user = self.user
		org.save()

	class Meta:
		model = models.EntityProfile
		exclude = ('user',)

class UserCreationForm(UserCreationForm):
    #email = forms.EmailField(required=True)   
	#address2 = forms.CharField(required=False)
	#country = forms.ModelChoiceField(queryset=models.Country.objects.all(), empty_label="Select...")

	class Meta:
		model = User
		fields = ("username", "password1", "password2")


## It appears one form class can be used for creating a profile and signing up
class SignupForm(forms.ModelForm):

	name = forms.CharField(required=False)
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)

	is_organization = forms.IntegerField()

	address2 = forms.CharField(required=False)

	country = forms.ModelChoiceField(queryset=models.Country.objects.all(), empty_label="Select...")

	def __init__(self,user=None,*args,**kwargs):
		self.user = user
		super(SignupForm,self).__init__(*args,**kwargs)

	def save(self):
		profile = super(SignupForm,self).save(commit=False)
		profile.user = self.user
		profile.save()

		if bool(self.cleaned_data['is_organization']):
			org = models.Organization()
			org.name = self.cleaned_data.get('name')
			org.user = self.user
			org.save()

		else:
			person = models.Person()
			#this is a hack for now until I create a date picker
			import datetime
			person.dob = datetime.datetime.now()
			person.first_name = self.cleaned_data.get('first_name')
			person.last_name = self.cleaned_data.get('last_name')
			#person.dob = self.cleaned_data.get('dob')
			person.user = self.user
			self.user.first_name = person.first_name
			self.user.last_name = person.last_name
			self.user.save()
			person.save()

	class Meta:
		model = models.EntityProfile	
