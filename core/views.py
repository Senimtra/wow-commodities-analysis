from django.http import HttpResponse
from django.template import loader
from django.db.models import Count
from .models import Commodities

import json

def home(request):
   template = loader.get_template('home.html')
   return HttpResponse(template.render())

def analysis(request):
   # Get a unique timestamps
   timestamps = Commodities.objects.values_list('timestamp', flat = True).distinct().order_by('timestamp')
   timestamp_list = [str(timestamp) for timestamp in timestamps]
   # Get number of auctions per timestamp
   auction_counts = Commodities.objects.filter(timestamp__in = timestamps).values('timestamp').annotate(num_auctions = Count('id')).order_by('timestamp')
   count_list = [auction_count['num_auctions'] for auction_count in auction_counts]
   # Set up view data
   template = loader.get_template('analysis.html')
   context = {'timestamp_list': json.dumps(timestamp_list), 'auctions_count_list': json.dumps(count_list)}
   return HttpResponse(template.render(context, request))

def data_status(request):
   template = loader.get_template('data_status.html')
   return HttpResponse(template.render())
