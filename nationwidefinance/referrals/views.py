from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.conf import settings


def home(request,template='index.html'):
	return render_to_response(template,
                              dict(title='Welcome to ',),
                              context_instance=RequestContext(request))

def redirect_to_home(request):
	return HttpResponseRedirect('/')

def logout(request,template='index.html'):
	django_logout(request)
	return render_to_response(template,
                              dict(title='Welcome to ',),
                              context_instance=RequestContext(request))


def openid_login(request, provider):
	if provider == 'gmail':
		url = '/login/google/'	
	elif provider == 'yahoo':
		url = '/login/yahoo/'	

	return HttpResponseRedirect(url)