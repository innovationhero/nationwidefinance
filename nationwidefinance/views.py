from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson


def home(request,template='index.html'):
	return render_to_response(template,
                              dict(title='Welcome to ',),
                              context_instance=RequestContext(request))