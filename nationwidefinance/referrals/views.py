from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse

from celery.result import AsyncResult

from nationwidefinance.referrals import models
from nationwidefinance.referrals import utils

from nationwidefinance.referrals.tasks import CalculateGifts


def home(request,template='index.html'):

	return render_to_response(template,
                              dict(title='Welcome to Nationwide Finance',),
                              context_instance=RequestContext(request))


def redirect_to_home(request):
	return HttpResponseRedirect('/nationwide/referrals')

def logout(request,template='index.html'):
	django_logout(request)
	return HttpResponseRedirect('/nationwide/referrals')


def check_user_profile(request):
	is_entity = False
	
	if request.user.is_authenticated:
		
		try:
			profile = request.user.get_profile()
			is_entity = True
		except:
			pass

		if not is_entity:
			#status = 0 means organization needs to create a profile
			return HttpResponse(simplejson.dumps([dict(status = 0)]),content_type = 'application/javascript; charset=utf8')

		#status = 10 means organization already has a profile
		return HttpResponse(simplejson.dumps([dict(statuc = 10)]),content_type = 'application/javascript; charset=utf8')
	

def create_profile(request,template='create_profile.html'):
	from nationwidefinance.referrals import forms
	if request.method == 'GET':
		form = forms.CreateProfileForm(instance=None)
		return render_to_response(template,
                              dict(title='Creating a Profile',form = form),
                              context_instance=RequestContext(request))

	else:

		form = forms.CreateProfileForm(user=request.user,data=request.POST)
		if form.is_valid():
			profile = form.save() 
			#do nothing as the record would have been saved already

		else:
			return render_to_response(template,
                              dict(title='Creating a Profile',form = form),
                              context_instance=RequestContext(request))

		# redirect to home for now as add_referral is failing 
		return HttpResponseRedirect('/')
		#return HttpResponseRedirect('/referrals/add_referral')

def edit_profile(request, template='create_profile.html'):
	from nationwidefinance.referrals import forms

	if request.method == 'GET':
		form = forms.CreateProfileForm(instance=request.user.get_profile())
		
	else:
		form = forms.CreateProfileForm(data=request.POST, instance=request.user.get_profile())
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')

	return render_to_response(template,
                              dict(title='Creating a Profile',form = form),
                              context_instance=RequestContext(request))

def add_referral(request):

	from nationwidefinance.referrals import forms
	
	if request.method == 'GET':
		form = forms.CreateUserForm(prefix='referrer')
		form1 = forms.CreateUserForm(prefix='referred')

	else:
		
		#check that org has not exceeded max referrals allowed
		profile = request.user.get_profile()
		referral_allowed = False

		if profile.plan.unlimited_referrals:
			referral_allowed = True

		if profile.plan.max_referrals_allowed > profile.referrals_made:
			referral_allowed = True

		if not referral_allowed:
			return render_to_response('referral_not_allowed.html',
                	dict(title='Referral Not Allowed',message = 'You have exceeded your referrals'),
                		context_instance=RequestContext(request))

		import random
		tmp_password = random.getrandbits(128)

		form = forms.CreateUserForm(user=request.user, tmp_password=tmp_password, data=request.POST, prefix='referrer')
		form1 = forms.CreateUserForm(user=request.user, tmp_password=tmp_password, data=request.POST, prefix='referred')
		if form.is_valid() and form1.is_valid():
			referrer = form.save()
			referred = form1.save()

			try:
				referral = models.EntityReferral.objects.get(organization__email=request.user.email,
					referrer__email=referrer.email,
					referred__email=referred.email)

				return render_to_response('referral_not_allowed.html',
                	dict(title='Referral Not Allowed',
                		message = 'This referral has already been recorded'),
                		context_instance=RequestContext(request))

			except models.EntityReferral.DoesNotExist:
				#save the ferral
				referral = models.EntityReferral()
				referral.referrer = referrer
				referral.entity_active = True
				referral.organization = request.user
				referral.created_date = datetime.now()
				referral.updated_date = datetime.now()
				referral.save()
				referral.referred = [referred]
				referral.save()


			# try:
			# 	org_referrers = models.OrganizationReferrerEntity.objects.get(organization__email=request.user.email)
			# except models.OrganizationReferrerEntity.DoesNotExist:
			# 	org_referrers = models.OrganizationReferrerEntity(organization=request.user)
			# 	org_referrers.save()

			# org_referrers.referrers.add(referrer)
			# org_referrers.save()

			# try:
			# 	org_referred_to = models.OrganizationReferredRelation.objects.get(organization__email=request.user.email)
			# except models.OrganizationReferredRelation.DoesNotExist:
			# 	org_referred_to = models.OrganizationReferredRelation(organization=request.user)
			# 	org_referred_to.save()

			# org_referred_to.referred.add(referred)
			# org_referred_to.save()


			# referral_id = request.POST.get('referral_id',None)

			# +1 on number of referrals this organization has recorded
			profile.referrals_made += 1
			profile.save()

			# if referral_id:
			# 	referral = models.EntityReferral.objects.get(pk=referral_id)
			# 	referral.referred.add(referred)
			# 	referral.save()
			# else:
				

			#send email to referrer and referred
			from nationwidefinance.mailer import send_new_user_email
			#send_new_user_email(referrer=referrer, referred=referred, business_name=request.user.get_profile().business_name)

			if request.POST.get('action') == 'add_another':
				form1 = forms.CreateUserForm(prefix='referred')
				return render_to_response('add_referral.html',
                	dict(title='Adding A Referral',
                		form = form,
                		form1 = form1,
                		referral_id = referral.pk),
                		context_instance=RequestContext(request))
			else:
				#add a referrer point for this referral
				try:
					referral_point = models.ReferrerPoints.objects.get(referrer__pk=referrer.pk)
					referral_point.value += request.user.get_profile().direct_referal_value
					referral_point.save()
				except models.ReferrerPoints.DoesNotExist:
					referral_point = models.ReferrerPoints(referrer=referrer, entity_active=True, value=request.user.get_profile().direct_referal_value)

					referral_point.save()

				utils.calculate_points([referrer.pk,], value=request.user.get_profile().indirect_referral_value)


				return HttpResponseRedirect('/nationwide/referrals')
	return render_to_response('add_referral.html',
                dict(title='Adding A Referral',
                	form = form,
                	form1 = form1),
                context_instance=RequestContext(request))

def calculate_gifts(request, template='calcluate_gifts_wait.html'):
	
	task = CalculateGifts.delay(request.user)
	request.session['task_id'] = task.id
	return render_to_response(template,
                    dict(),
                    context_instance=RequestContext(request))

def calculate_gifts_check(request):
	if request.method == 'GET':
		task_id = request.session.get('task_id', None)
		if task_id:
			result = AsyncResult(task_id)
			if result.ready():
				return HttpResponse(simplejson.dumps([dict(status = 200)]), content_type = 'application/javascript; charset=utf8')
			else:
				return HttpResponse(simplejson.dumps([dict(status = 100)]), content_type = 'application/javascript; charset=utf8')
	return HttpResponse(simplejson.dumps([dict(status = 500)]), content_type = 'application/javascript; charset=utf8')


def referrer_first_login(request):
	from nationwidefinance.referrals import forms
	if request.method == 'GET':
		form = forms.FirstLoginForm()
		return render_to_response('referrer_first_login.html',
                dict(title='First Login',form = form),
                context_instance=RequestContext(request))

	else:
		form = forms.FirstLoginForm(data=request.POST)
		if form.is_valid():
			form.save()
			user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
			login(request, user)
			return HttpResponseRedirect('/')
		return render_to_response('referrer_first_login.html',
                dict(title='First Login',form = form),
                context_instance=RequestContext(request))

def view_referrers(request):
	referrals = models.EntityReferral.objects.filter(organization__email=request.user.email)

	if len(referrals) == 0:
		return render_to_response('no_referrers.html',
                dict(title='Error!',),
                context_instance=RequestContext(request))
		
	aaData = []
	for referral in referrals:
		sublist = []
		sublist.append(str(referral.referrer.first_name))
		sublist.append(str(referral.referrer.last_name))
		sublist.append(str(models.ReferrerPoints.objects.get(referral.referrer__email=referrer.email).value))
		aaData.append(sublist)


	return render_to_response('referrers.html',
            dict(title='Viewing Referrers',aaData = aaData),
            context_instance=RequestContext(request))

def view_referred(request):

	referrals = models.EntityReferral.objects.filter(referrer__email=request.user.email)
	if len(referrals) == 0:
		return render_to_response('none_referred.html',
                dict(title='Error!',),
                context_instance=RequestContext(request))

	aaData = []
	for referral in referrals:
		referred = referral.referred.all()
		for r in referred:
			sublist = []
			sublist.append(str(r.first_name))
			sublist.append(str(r.last_name))
			sublist.append(str(referral.organization.get_profile().business_name))
			aaData.append(sublist)


	return render_to_response('referred.html',
            dict(title='Viewing Referrers',aaData = aaData),
            context_instance=RequestContext(request))

def add_referral_autocomplete(request):
	if request.method == 'POST':
		search = request.POST.get('email')
		users = User.objects.filter(email__icontains=search)
		result = [dict(email = user.email, first_name = user.first_name, last_name = user.last_name, dob = datetime.strftime(user.dob,'%d/%m/%Y') if user.dob else '') for user in users]
		return HttpResponse(simplejson.dumps(result))
	return HttpResponse(simplejson.dumps([dict(status = 500)]))

