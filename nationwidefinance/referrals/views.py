from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.conf import settings

from nationwidefinance.referrals import models
from nationwidefinance.referrals import forms


def home(request,template='index.html'):
	#profile = request.user.get_profile()
	#print profile
	#print '>>>>>>>>>>>>>>>>>>>> %s' % profile.address1

	return render_to_response(template,
                              dict(title='Welcome to Nationwide Finance',),
                              context_instance=RequestContext(request))

def redirect_to_home(request):
	return HttpResponseRedirect('/')

def logout(request,template='index.html'):
	django_logout(request)
	return render_to_response(template,
                              dict(title='Welcome to ',),
                              context_instance=RequestContext(request))


def check_user_profile(request):
	is_entity = False
	print models.Organization.objects.all()
	if request.user.is_authenticated:
		
		try:
			models.Organization.objects.get(user__username=request.user.username)
			is_entity = True
		except models.Organization.DoesNotExist:
			pass

		try:
			models.Person.objects.get(user=request.user)
			is_entity = True
		except models.Person.DoesNotExist:
			pass		

		if not is_entity:
			#user has not created a profile 
			#status 0 means user need to create a profile
			return HttpResponse(simplejson.dumps([dict(status = 0)]),content_type = 'application/javascript; charset=utf8')

		#user is new to site, and has not created a profile
		#status 10 indicated user must create a profile
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

		else:
			return render_to_response(template,
                              dict(title='Creating a Profile',form = form),
                              context_instance=RequestContext(request))

		return render_to_response('add_referral.html',
                              dict(title='Creating a Profile',form = form),
                              context_instance=RequestContext(request))