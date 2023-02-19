from django.http import HttpResponse
from django.template import loader

def analysis(request):
   template = loader.get_template('analysis.html')
   return HttpResponse(template.render())

def data_status(request):
   template = loader.get_template('data_status.html')
   return HttpResponse(template.render())
