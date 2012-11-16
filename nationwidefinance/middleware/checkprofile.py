from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class CheckProfileMiddleware():

	def process_request(self, request):

		if request.path == '/referrals/create_profile/': return None

		print '>>>>>>>>>>>>>>>>>>>>>>>  ', request.user

		if not request.user: return None
		
		try:
			profile = request.user.get_profile()
			return None
		except:
			return HttpResponseRedirect(reverse('create_profile'))

