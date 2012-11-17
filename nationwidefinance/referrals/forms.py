from datetime import datetime 

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from nationwidefinance.referrals import models

class CreateEntity(forms.Form):
	
	
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)
	email_address = forms.CharField(required=True)
	dob = forms.DateTimeField(required=False)


	def __init__(self, user=None, *args, **kwargs):
		super(CreateEntity, self).__init__(*args,**kwargs)
		self.user = user

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
			entity.organization = self.user
			entity.entity_active = True
			entity.updated_date = datetime.now()
			entity.created_date = datetime.now()
			entity.save()
			return entity


	class Meta:
		model = models.EntityProfile
		exclude = ('organization', 'entity_active', 'created_date', 'updated_date',)

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

	metrics = forms.ChoiceField(required=True, choices=[('inherit', 'Inherit from plan'), ('custom', 'Custom Choice')])
	entity_type = forms.ChoiceField(required=True, choices=[('','Select'), ('org', 'Organization'), ('indv', 'Individual')])
	plan = forms.ModelChoiceField(required=False, widget=forms.Select, queryset=models.EntityPlan.objects.filter(entity_active=True))
	industry = forms.ModelChoiceField(required=False, widget=forms.Select, queryset=models.Industry.objects.filter(entity_active=True))
	country = forms.ModelChoiceField(required=True, widget=forms.Select, queryset=models.Country.objects.all())
	
	business_name = forms.CharField(required=False, widget=forms.TextInput(attrs=dict(style = 'width:200px;')))
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	email = forms.CharField(required=True)
	phone = forms.CharField(required=False)

	num_referrals_for_gift = forms.IntegerField(required=False)
	direct_referal_value = forms.FloatField(required=False)
	indirect_referral_value = forms.FloatField(required=False)

	address2 = forms.CharField(required=False)

	def __init__(self,user=None,*args,**kwargs):
		self.user = user
		super(CreateProfileForm,self).__init__(*args,**kwargs)
		self.fields['country'].initial = models.Country.objects.get(code='AU').pk


	def clean_business_name(self):
		if self.cleaned_data.get('entity_type') == 'org':
			if not self.cleaned_data.get('business_name', None):
				raise forms.ValidationError('This field is required')

		return self.cleaned_data.get('business_name')

	def clean_plan(self):
		if self.cleaned_data.get('entity_type') == 'org':
			if not self.cleaned_data.get('plan', None):
				raise forms.ValidationError('This field is required')

		return self.cleaned_data.get('plan')

	def clean_industry(self):
		if self.cleaned_data.get('entity_type') == 'org':
			if not self.cleaned_data.get('industry', None):
				raise forms.ValidationError('This field is required')

		return self.cleaned_data.get('industry')

	def clean_num_referrals_for_gift(self):
		if self.data.get('metrics') == 'custom':
			if not self.cleaned_data.get('num_referrals_for_gift'):
				raise forms.ValidationError('This field is required')

		return self.cleaned_data.get('num_referrals_for_gift')

	def clean_direct_referal_value(self):
		if self.data.get('metrics') == 'custom':
			if not self.cleaned_data.get('direct_referal_value'):
				raise forms.ValidationError('This field is required')

		return self.cleaned_data.get('direct_referal_value')	

	def clean_indirect_referral_value(self):
		if self.data.get('metrics') == 'custom':
			if not self.cleaned_data.get('indirect_reverral_value'):
				raise forms.ValidationError('This field is required')

		return self.cleaned_data.get('indirect_reverral_value')	

	def save(self):
		#save the contact
		contact = models.EntityContact(first_name=self.cleaned_data['first_name'], 
			last_name=self.cleaned_data['last_name'], 
			email=self.cleaned_data['email'],
			phone = self.cleaned_data.get('phone'))
		contact.save()

		profile = super(CreateProfileForm,self).save(commit=False)
		profile.user = self.user
		profile.entity_contact = contact
		profile.referrals_made = 0

		if self.cleaned_data.get('entity_type') == 'org' and self.data.get('metrics') == 'inherit':
			plan = self.cleaned_data.get('plan')
			profile.num_referrals_for_gift = plan.num_referrals_for_gift
			profile.direct_referal_value = plan.direct_referal_value
			profile.indirect_referral_value = plan.indirect_referral_value

		profile.entity_active = True
		profile.created_date = datetime.now()
		profile.updated_date = datetime.now()

		profile.save()
		

	class Meta:
		model = models.EntityProfile
		exclude = ('user','created_date', 'updated_date', 'entity_contact')