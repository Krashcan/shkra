from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
from .forms import SubmitUrlForm
from .models import KirrURL
from analytics.models import ClickEvent

# Create your views here.
class HomeView(View):
	def get(self,request,*args,**kwargs):
		form = SubmitUrlForm()
		context = {
			"form":form,
			"title":"Shkra"
		}
		return render(request,"shortener/home.html",context)
	def post(self,request,*args,**kwargs):
		form = SubmitUrlForm(request.POST)
		template = "shortener/home.html"
		context = {
			"form":form,
			"title":"Shkra"
		}
		if form.is_valid():
			valid_url = form.cleaned_data['url']
			obj,created = KirrURL.objects.get_or_create(url=valid_url)
			context ={
				"object":obj,
				"created":created
			}

			template = "shortener/result.html"
		return render(request,template,context)

class KirrRedirectView(View):
	def get(self,request,shortcode=None):
		obj = get_object_or_404(KirrURL,shortcode=shortcode)
		print(ClickEvent.objects.create_event(obj))
		return HttpResponseRedirect(obj.url)