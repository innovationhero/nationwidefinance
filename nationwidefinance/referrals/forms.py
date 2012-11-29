from datetime import datetime 

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from nationwidefinance.referrals import models
from social_auth.models import UserSocialAuth

class FirstLoginForm(forms.Form):

	email = forms.CharField(required=True)
	password1 = forms.CharField(required=True, widget=forms.PasswordInput)
	password2 = forms.CharField(required=True, widget=forms.PasswordInput)

	def clean_email(self):
		try:
			user = User.objects.get(email=self.cleaned_data.get('email'))
			return self.cleaned_data.get('email')
		except User.DoesNotExist:
			raise forms.ValidationError('This email address is not attached to an account')

	def clean_password1(self):
		if self.data.get('password1') != self.data.get('password2'):
			raise forms.ValidationError('Passwords do not match')

		if len(self.data.get('password1')) < 6:
			raise forms.ValidationError('Password must be at least 6 characters')

		return self.cleaned_data.get('password1')

	def save(self):
		user = User.objects.get(email=self.cleaned_data.get('email'))
		user.set_password(self.cleaned_data.get('password1'))
		user.is_active = True
		user.save()

class CreateUserForm(forms.ModelForm):
	
	
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	email = forms.CharField(required=True)
	dob = forms.DateTimeField(required=True, input_formats=settings.DATE_INPUT_FORMATS)


	def __init__(self, user=None, tmp_password=None, *args, **kwargs):
		super(CreateUserForm, self).__init__(*args,**kwargs)
		self.organization = user
		if tmp_password:
			self.tmp_password = tmp_password



	def save(self):
		try:
			entity = User.objects.get(email=self.cleaned_data.get('email'))
			return entity
		except User.DoesNotExist, e:
			entity = super(CreateUserForm,self).save(commit=False)
			entity.username = self.cleaned_data.get('email')
			entity.set_password(self.tmp_password)
			entity.date_joined = datetime.now()
			entity.dob = self.cleaned_data.get('dob')
			entity.is_active = False
			entity.is_superuser = False
			entity.is_staff = False
			entity.save()
			return entity


	class Meta:
		model = User
		exclude = ('is_active', 'last_login', 'date_joined','is_superuser','is_staff','username','password')

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

	inherit_from_plan = forms.ChoiceField(required=True, choices=[('1', 'Inherit from plan'), ('0', 'Custom Choice')])
	post_to_facebook = forms.BooleanField(required=False)
	entity_type = forms.ChoiceField(required=True, choices=[('','Select'), ('org', 'Organization'), ('indv', 'Individual')])
	plan = forms.ModelChoiceField(required=False, widget=forms.Select, queryset=models.EntityPlan.objects.filter(entity_active=True))
	industry = forms.ModelChoiceField(required=False, widget=forms.Select, queryset=models.Industry.objects.filter(entity_active=True))
	country = forms.ModelChoiceField(required=True, widget=forms.Select, queryset=models.Country.objects.all())

	referrals_made = forms.CharField(widget=forms.HiddenInput(), required=False)
	
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

		if self.instance.pk:

			self.initial['inherit_from_plan'] = '1' if self.instance.inherit_from_plan else '0'

			self.initial['first_name'] = self.instance.entity_contact.first_name
			self.initial['last_name'] = self.instance.entity_contact.last_name
			self.initial['email'] = self.instance.entity_contact.email
			self.initial['phone'] = self.instance.entity_contact.phone
			self.initial['contry'] = self.instance.country.pk

		else:
			self.initial['country'] = models.Country.objects.get(code='AU').pk


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
		if not bool(int(self.data.get('inherit_from_plan'))):
			if not self.cleaned_data.get('num_referrals_for_gift'):
				raise forms.ValidationError('This field is required')

		return self.cleaned_data.get('num_referrals_for_gift')

	def clean_direct_referal_value(self):
		if not bool(int(self.data.get('inherit_from_plan'))):
			if not self.cleaned_data.get('direct_referal_value'):
				raise forms.ValidationError('This field is required')

		return self.cleaned_data.get('direct_referal_value')	

	def clean_indirect_referral_value(self):
		if not bool(int(self.data.get('inherit_from_plan'))):
			if not self.cleaned_data.get('indirect_referral_value'):
				raise forms.ValidationError('This field is required')

		return self.cleaned_data.get('indirect_referral_value')	

	def save(self):
		if not self.instance.pk:
			#create a new contact the contact
			contact = models.EntityContact(first_name=self.cleaned_data['first_name'], 
				last_name=self.cleaned_data['last_name'], 
				email=self.cleaned_data['email'],
				phone = self.cleaned_data.get('phone'))
			contact.save()
		else:
			self.instance.entity_contact.first_name = self.cleaned_data['first_name']
			self.instance.entity_contact.last_name = self.cleaned_data['last_name']
			self.instance.entity_contact.email = self.cleaned_data['email']
			self.instance.entity_contact.phone = self.cleaned_data['phone']
			self.instance.entity_contact.save()

		self.instance = super(CreateProfileForm,self).save(commit=False)

		if not self.instance.pk:
			self.instance.user = self.user
			self.instance.entity_contact = contact
			self.instance.referrals_made = 0
			
			self.instance.created_date = datetime.now()

		if self.cleaned_data.get('entity_type') == 'org' and bool(int(self.data.get('inherit_from_plan'))):
			plan = self.cleaned_data.get('plan')
			self.instance.num_referrals_for_gift = plan.num_referrals_for_gift
			self.instance.direct_referal_value = plan.direct_referal_value
			self.instance.indirect_referral_value = plan.indirect_referral_value
		
		self.instance.entity_active = True
		self.instance.updated_date = datetime.now()

		self.instance.save()
		

	class Meta:
		model = models.EntityProfile
		exclude = ('user','created_date', 'updated_date', 'entity_contact')

class FacebookPostForm(forms.ModelForm):

	user = forms.ModelChoiceField(queryset=UserSocialAuth.objects.filter(provider='facebook'), widget=forms.HiddenInput())
	message = forms.CharField(widget=forms.Textarea())
	link = forms.URLField(required=False)

	def __init__(self,user=None, *args, **kwargs):
		super(FacebookPostForm,self).__init__(*args, **kwargs)
		if user:
			self.initial['user'] = user.pk

	def clean_user(self):
		if not self.cleaned_data.get('user'):
			raise forms.ValidationError('You must be logged in as a Facebook user')

		return self.cleaned_data.get('user')

	class Meta:
		model = models.FacebookPostMessage
