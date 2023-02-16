from django.http import HttpResponse
from django.template import loader

def analysis(request):
   template = loader.get_template('analysis.html')
   return HttpResponse(template.render())
