from django.db import models
from django.conf import settings
import string
import random
from django_hosts.resolvers import reverse
from .utils import create_shortcode
from .validators import validate_url

SHORTCODE_MAX = getattr(settings,"SHORTCODE_MAX",15)

class KirrURLManager(models.Manager):
	def all(self,*args,**kwargs):
		return super(KirrURLManager,self).all(*args,**kwargs).filter(active=True)

	def refresh_shortcodes(self):
		qs = KirrURL.objects.filter(id__gte=1)
		new_codes = 0
		for q in qs:
			q.shortcode = create_shortcode(q)
			q.save()
			new_codes += 1
		return "New codes made: {i}".format(i=new_codes)

class KirrURL(models.Model):
	url 		= models.CharField(max_length=220,validators=[validate_url] )
	shortcode 	= models.CharField(max_length=SHORTCODE_MAX, unique = True, blank = True)
	updated 	= models.DateTimeField(auto_now=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)
	active		= models.BooleanField(default=True)
	
	objects = KirrURLManager()

	def __str__(self):
		return str(self.url)

	def save(self,*args,**kwargs):
		self.shortcode = create_shortcode(self)
		if not "http" in self.url:
			self.url = "http://"+self.url
		super(KirrURL,self).save(*args,**kwargs)

	def get_short_url(self):
		url = reverse("shortcode", kwargs={'shortcode':self.shortcode},host='www',scheme='http')
		return url

