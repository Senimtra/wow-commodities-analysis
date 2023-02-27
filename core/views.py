from django.http import HttpResponse
from django.template import loader
from django.db.models import Count
from .models import Commodities

import json

def home(request):
   template = loader.get_template('home.html')
   return HttpResponse(template.render())

def market(request):
   # Get a unique timestamps
   timestamps = Commodities.objects.values_list('timestamp', flat = True).distinct().order_by('timestamp')
   timestamp_list = [str(timestamp) for timestamp in timestamps]
   # Get number of auctions per timestamp
   auction_counts = Commodities.objects.filter(timestamp__in = timestamps).values('timestamp').annotate(num_auctions = Count('id')).order_by('timestamp')
   count_list = [auction_count['num_auctions'] for auction_count in auction_counts]
   # Set up view data
   template = loader.get_template('market.html')
   context = {'timestamp_list': json.dumps(timestamp_list), 'auctions_count_list': json.dumps(count_list)}
   return HttpResponse(template.render(context, request))

def distribution(request):
   template = loader.get_template('distribution.html')
   return HttpResponse(template.render())

def profit(request):
   template = loader.get_template('profit.html')
   return HttpResponse(template.render())

def data(request):
   template = loader.get_template('data.html')
   return HttpResponse(template.render())
