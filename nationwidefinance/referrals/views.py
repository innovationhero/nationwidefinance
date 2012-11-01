from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


from nationwidefinance.referrals import models
from nationwidefinance.referrals import forms


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

def nationwidelogin(request,template='login.html'):
	#do login
	if request.method == 'POST': # If the form has been submitted...
		form = LoginForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					# Redirect to a success page.
					login(request, user)				
					return HttpResponseRedirect('/')

				else:
					# Return a 'disabled account' error message				
					error = u'account disabled'
					return errorHandle(request, error)
			else:
				 # Return an 'invalid login' error message.			
				error = u'invalid login'
				return errorHandle(request, error)
		else: 
			username = ''
			password = ''
			error = u'form is invalid'
			return errorHandle(request, error)		
	else:
		form = LoginForm() # An unbound form
		return render_to_response('login.html', dict(title='Nationwide Login ',), context_instance=RequestContext(request))	


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
			#do nothing as the record would have been saved already

		else:
			return render_to_response(template,
                              dict(title='Creating a Profile',form = form),
                              context_instance=RequestContext(request))

		# redirect to home for now as add_referral is failing 
		return HttpResponseRedirect('/')
		#return HttpResponseRedirect('/referrals/add_referral')

def add_referral(request):
	users = User.objects.all()
	aaData = []
	for user in users:
		if user.is_staff or user.is_superuser: continue
		list = []
		type = ''
		list.append(user.id)
		try:
			org = models.Organization.objects.get(user__username=user.username)
			type = 'Organization'
			list.append(type)
			list.append(str(org.name))
			list.append(str(''))
		except models.Organization.DoesNotExist:
			pass

		try:
			person = models.Person.objects.get(user__username=user.username)
			type = 'Person'
			list.append(type)
			list.append(str(person.first_name))
			list.append(str(person.last_name))
		except models.Person.DoesNotExist:
			pass

		
		aaData.append(list)
	return render_to_response('add_referral.html',
                         dict(title='Adding A Referral',aaData = aaData),
                          context_instance=RequestContext(request))


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
