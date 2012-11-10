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


from nationwidefinance.referrals import models
from nationwidefinance.referrals import forms
from nationwidefinance.referrals import utils

from nationwidefinance.referrals.tasks import CalculateGifts


def home(request,template='index.html'):

	return render_to_response(template,
                              dict(title='Welcome to Nationwide Finance',),
                              context_instance=RequestContext(request))


def errorHandle(request, error):
		form = LoginForm()
		return render_to_response('login.html', {
				'error' : error,
				'form' : form,
		}, context_instance=RequestContext(request))


def redirect_to_home(request):
	return HttpResponseRedirect('/')

def logout(request,template='index.html'):
	django_logout(request)
	return HttpResponseRedirect('/')


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
	if request.method == 'GET':
		form = forms.CreateProfileForm()
		return render_to_response(template,
                              dict(title='Creating a Profile',form = form),
                              context_instance=RequestContext(request))

	else:
		form = forms.CreateProfileForm(user=request.user,data=request.POST)
		if form.is_valid():
			form.save() 
			#do nothing as the record would have been saved already

		else:
			return render_to_response(template,
                              dict(title='Creating a Profile',form = form),
                              context_instance=RequestContext(request))

		# redirect to home for now as add_referral is failing 
		return HttpResponseRedirect('/')
		#return HttpResponseRedirect('/referrals/add_referral')

def add_referral(request):
	
	if request.method == 'GET':
		form = forms.CreateEntity(prefix='referrer', initial={'entity_type' : 'org'})
		form1 = forms.CreateEntity(prefix='referred', initial={'entity_type' : 'org'})

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
                	dict(title='Referral Not Allowed',),
                		context_instance=RequestContext(request))

		form = forms.CreateEntity(user=request.user, data=request.POST, prefix='referrer')
		form1 = forms.CreateEntity(user=request.user, data=request.POST, prefix='referred')
		if form.is_valid() and form1.is_valid():
			referrer = form.save()
			referred = form1.save()

			referral_id = request.POST.get('referral_id',None)

			# +1 on number of referrals this organization has recorded
			profile.referrals_made += 1
			profile.save()

			if referral_id:
				referral = models.EntityReferral.objects.get(pk=referral_id)
				referral.referred.add(referred)
				referral.save()
			else:
				#save the ferral
				referral = models.EntityReferral()
				referral.referrer = referrer
				referral.entity_active = True
				referral.created_date = datetime.now()
				referral.updated_date = datetime.now()
				referral.save()
				referral.referred = [referred]
				referral.save()

			if request.POST.get('action') == 'add_another':
				form1 = forms.CreateEntity(prefix='referred', initial={'entity_type' : 'org'})
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
					referral_point.value += 1
					referral_point.save()
				except models.ReferrerPoints.DoesNotExist:
					referral_point = models.ReferrerPoints(referrer=referrer, entity_active=True, value=1)

					referral_point.save()
				utils.calculate_points([referrer.pk,])
				return HttpResponseRedirect('/')
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
	if request.method == 'POST':
		task_id = request.session.get('task_id',None)
		if task_id:
			result = AsyncResult(task_id)
			if result.ready():
				return HttpResponse(simplejson.dumps([dict(status = 200)]), content_type = 'application/javascript; charset=utf8')
		else:
			return HttpResponse(simplejson.dumps([dict(status = 100)]), content_type = 'application/javascript; charset=utf8')
	return HttpResponse(simplejson.dumps([dict(status = 500)]), content_type = 'application/javascript; charset=utf8')

def sign_up(request,template='sign_up.html'):	

	if request.method == 'GET':
		form = forms.UserCreationForm()
		return render_to_response(template,
                              dict(title='Sign up',form = form),
                              context_instance=RequestContext(request))

	else:
		form = forms.UserCreationForm(data=request.POST)
		if form.is_valid():
			#user = form.save()		form.data['field_name']
			user = User.objects.create_user(form.data['username'], '', form.data['password1'])

			user = authenticate(username=form.data['password1'], password=form.data['password1'])

			##commented the login of user out as it throws error when loading the home page
			login(request,user)

		else:
			return render_to_response(template,
                              dict(title='Sign up',form = form),
                              context_instance=RequestContext(request))

		
		return HttpResponseRedirect('/referrals/create_profile')
