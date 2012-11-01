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
	return HttpResponseRedirect('/')


def check_user_profile(request):
	is_entity = False
	
	if request.user.is_authenticated:
		
		try:
			models.Organization.objects.get(user__username=request.user.username)
			is_entity = True
		except models.Organization.DoesNotExist:
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
		
		form = forms.CreateEntity(data=request.POST, prefix='referrer')
		form1 = forms.CreateEntity(data=request.POST, prefix='referred')
		if form.is_valid() and form1.is_valid():
			referrer = form.save()
			referred = form1.save()

			referral_id = request.POST.get('referral_id',None)

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

				#calculate points accumelated by this new referral
				referral_points = models.ReferrerPoints()
				referral_points.referrer = referrer
				referral_points.value = utils.calculate_points([referrer.pk,], 1)
				referral_points.entity_active = True
				referral_points.save()


			if request.POST.get('action') == 'add_another':
				form1 = forms.CreateEntity(prefix='referred', initial={'entity_type' : 'org'})
				return render_to_response('add_referral.html',
                	dict(title='Adding A Referral',
                		form = form,
                		form1 = form1,
                		referral_id = referral.pk),
                		context_instance=RequestContext(request))
			else:
				return HttpResponseRedirect('/')
	return render_to_response('add_referral.html',
                dict(title='Adding A Referral',
                	form = form,
                	form1 = form1),
                context_instance=RequestContext(request))

"""
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
"""

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
		
<<<<<<< HEAD
		aaData.append(list)
	return render_to_response('add_referral.html',
                         dict(title='Adding A Referral',aaData = aaData),
                          context_instance=RequestContext(request))


=======
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
	
>>>>>>> dfdb474c289894353adafac5eba055c4e19397ae
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
