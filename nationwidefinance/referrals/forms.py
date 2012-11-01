from django import forms

from nationwidefinance.referrals import models

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AddReferralForm(forms.ModelForm):

	class Meta:
		model = models.EntityReferral

## It appears one form class can be used for creating a profile and signing up
class CreateProfileForm(forms.ModelForm):

	name = forms.CharField(required=False)
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)

	is_organization = forms.IntegerField()

	address2 = forms.CharField(required=False)

	country = forms.ModelChoiceField(queryset=models.Country.objects.all(), empty_label="Select...")

	def __init__(self,user=None,*args,**kwargs):
		self.user = user
		super(CreateProfileForm,self).__init__(*args,**kwargs)

	def save(self):
		profile = super(CreateProfileForm,self).save(commit=False)
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
