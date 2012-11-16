from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class CheckProfileMiddleware():

	def process_request(self, request):

		if request.path == '/referrals/create_profile/' or request.path == '/referrals/logout/' or 'admin' in request.path: return None

		if not request.user.is_authenticated(): return None
		
		try:
			profile = request.user.get_profile()
			return None
		except:
			return HttpResponseRedirect(reverse('create_profile'))

