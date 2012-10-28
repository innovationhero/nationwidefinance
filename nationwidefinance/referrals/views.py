from django.http import HttpResponse, HttpResponseRedirect
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

def openid_login(request, provider):

	settings.OPENID_SSO_SERVER_URL = settings.OPENID_GMAIL_URL	

	if provider == 'gmail':
		settings.OPENID_SSO_SERVER_URL = settings.OPENID_GMAIL_URL
	elif provider == 'yahoo':
		settings.OPENID_SSO_SERVER_URL = settings.OPENID_YAHOO_URL

	return HttpResponseRedirect('/openid/login/')