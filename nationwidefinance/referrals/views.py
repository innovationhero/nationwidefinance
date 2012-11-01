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


def home(request,template='index.html'):

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

		
		return HttpResponseRedirect('/referrals/add_referral')

def add_referral(request):
	if request.method == 'GET':
		return render_to_response('add_referral.html',
                dict(title='Adding A Referral'),
                context_instance=RequestContext(request))
	else:
		aaData = []
		action = request.POST.get('action','')
		if action == 'org_search':
			name = request.POST.get('org_name','')
			orgs = models.Organization.objects.filter(name__icontains=name)
			for org in orgs:
				sublist = []
				sublist.append(org.user.id)
				sublist.append(str(org.name))
				aaData.append(sublist)
		elif action == 'person_search':
			first_name = request.POST.get('first_name','')
			last_name = request.POST.get('last_name','')
			email = request.POST.get('email','')
			persons = models.Person.objects.filter(
				first_name__icontains=first_name,
				last_name__icontains=last_name,
				user__email__icontains=email)
			for p in persons:
				sublist = []
				sublist.append(p.user.id)
				sublist.append(str(p.user.email))
				sublist.append(str(p.first_name))
				sublist.append(str(p.last_name))
				aaData.append(sublist)
		else:
			return HttpResponseRedirect(reverse('add_referred', kwargs={'user_id' : request.POST.get('user_id'),}))

		return render_to_response('add_referral.html',
                dict(title='Adding A Referral',
                	 action = action,
                	 aaData = aaData),
                context_instance=RequestContext(request))

def add_referred(request, user_id=None, template='add_referred.html'):
	if not user_id:
		raise RuntimeError('Error')
	if request.method == 'GET':
		return render_to_response(template,
                dict(title='Sign up', user_id = user_id),
                context_instance=RequestContext(request))
	else:
		aaData = []
		user_id = request.POST.get('referrer')
		referred_ids = request.POST.get('referred',[])
		if request.POST.get('select_referred_id',None):
			referred_ids.append(request.POST.get('select_referred_id'))
		
		action = request.POST.get('action','')

		if action == 'org_search':
			name = request.POST.get('org_name','')
			orgs = models.Organization.objects.filter(name__icontains=name)
			for org in orgs:
				sublist = []
				sublist.append(org.user.id)
				sublist.append(str(org.name))
				aaData.append(sublist)

		elif action == 'person_search':

			first_name = request.POST.get('first_name','')
			last_name = request.POST.get('last_name','')
			email = request.POST.get('email','')

			persons = models.Person.objects.filter(
				first_name__icontains=first_name,
				last_name__icontains=last_name,
				user__email__icontains=email)
			for p in persons:
				sublist = []
				sublist.append(p.user.id)
				sublist.append(str(p.user.email))
				sublist.append(str(p.first_name))
				sublist.append(str(p.last_name))
				aaData.append(sublist)
		elif action == 'another':
			#reset the form for another search
			return render_to_response('add_referred.html',
                dict(title='Adding A Referral',
                	 action = action,
                	 aaData = [],
                	 referred_ids = referred_ids,
                	 user_id = user_id),
                context_instance=RequestContext(request))
		elif action == 'save':
			#time to create a form and save the referrer and referred
			form = forms.AddReferralForm(data=request.POST)
			print '>>>>>>>>>>>>>>>>>>>>> ', request.POST
			if form.is_valid():
				print '>>>>>>>>>>> VALID'
				form.save()
			else:
				print '>>>>>>>>>>>>>> INVALID'
				return HttpResponseRedirect('/')

		return render_to_response('add_referred.html',
                dict(title='Adding A Referral',
                	 action = action,
                	 aaData = aaData,
                	 referred_ids = referred_ids,
                	 user_id = user_id),
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
			form.save()
			username = request.POST['username']
			password = request.POST['password1']
			user = authenticate(username=username, password=password)
			##commented the login of user out as it throws error when loading the home page
			##login(request,user)

		else:
			return render_to_response(template,
                              dict(title='Sign up',form = form),
                              context_instance=RequestContext(request))

		
		return HttpResponseRedirect('/')
