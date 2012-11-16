from datetime import datetime 

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from nationwidefinance.referrals import models

# class CreateEntity(forms.ModelForm):

# 	entity_type = forms.ChoiceField(required=True, widget=forms.Select, choices=[('', u'Select'), ('org', 'Organization'), ('person', 'Person')])
# 	org_name = forms.CharField(required=False)
# 	first_name = forms.CharField(required=False)
# 	last_name = forms.CharField(required=False)
# 	email_address = forms.CharField(required=True)
# 	dob = forms.DateTimeField(required=False)


# 	def __init__(self, user=None, *args, **kwargs):
# 		super(CreateEntity, self).__init__(*args,**kwargs)
# 		self.user = user

# 	def clean_org_name(self):
# 		if self.cleaned_data.get('entity_type')  \
# 			and self.cleaned_data['entity_type'] == 'org' \
# 			and not self.cleaned_data.get('org_name'):
# 				raise forms.ValidationError('Organization name required')
# 		return self.cleaned_data['org_name']

# 	def clean_first_name(self):
# 		if self.cleaned_data.get('entity_type') \
# 			and self.cleaned_data['entity_type'] == 'person' \
# 			and not self.cleaned_data.get('first_name'):
# 				raise forms.ValidationError('First name required')
# 		return self.cleaned_data['first_name']

# 	def clean_last_name(self):
# 		if self.cleaned_data.get('entity_type') \
# 			and self.cleaned_data['entity_type'] == 'person' \
# 			and not self.cleaned_data['last_name']:
# 				raise forms.ValidationError('Last name required')
# 		return self.cleaned_data['last_name']	

# 	def clean_dob(self):
# 		if self.cleaned_data.get('entity_type') \
# 			and self.cleaned_data['entity_type'] == 'person' \
# 			and not self.cleaned_data.get('dob'):
# 				raise forms.ValidationError('DOB required')
# 		return self.cleaned_data['dob']	

# 	def save(self):
# 		try:
# 			entity = models.Entity.objects.get(email_address=self.cleaned_data['email_address'])
# 			return entity
# 		except models.Entity.DoesNotExist, e:
# 			entity = super(CreateEntity,self).save(commit=False)
# 			entity.organization = self.user
# 			entity.entity_active = True
# 			entity.updated_date = datetime.now()
# 			entity.created_date = datetime.now()
# 			entity.save()
# 			return entity


# 	class Meta:
# 		model = models.Entity
# 		exclude = ('organization', 'entity_active', 'created_date', 'updated_date',)

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

	address2 = forms.CharField(required=False)
	country = forms.ModelChoiceField(queryset=models.Country.objects.all(), empty_label="Select...")
	plan = forms.ModelChoiceField(queryset=models.EntityPlan.objects.filter(entity_active=True), empty_label="Select...")

	def __init__(self,user=None,*args,**kwargs):
		self.user = user
		super(CreateProfileForm,self).__init__(*args,**kwargs)

	def save(self):
		profile = super(CreateProfileForm,self).save(commit=False)
		profile.user = self.user
		profile.referrals_made = 0
		profile.save()
		

	class Meta:
		model = models.EntityProfile
		exclude = ('user',)