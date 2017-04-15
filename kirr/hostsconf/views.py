from django.http import HttpResponseRedirect
from django.conf import settings

DEFAULT_REDIRECT_URL = getattr(settings, 'DEFAULT_REDIRECT_URL','http://www.krash.io:8000/')
def wildcard_redirect(self,path=None):
	if path is not None:
		return HttpResponseRedirect(DEFAULT_REDIRECT_URL + path)
	return HttpResponseRedirect(DEFAULT_REDIRECT_URL)