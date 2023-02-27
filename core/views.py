from django.http import HttpResponse
from django.template import loader
from .models import Commodities

def home(request):
   template = loader.get_template('home.html')
   return HttpResponse(template.render())

def analysis(request):
   data = Commodities.objects.all().values()[0]
   template = loader.get_template('analysis.html')
   context = {'data': data}
   return HttpResponse(template.render(context, request))

def data_status(request):
   template = loader.get_template('data_status.html')
   return HttpResponse(template.render())
