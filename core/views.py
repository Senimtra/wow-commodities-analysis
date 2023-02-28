from django.http import HttpResponse
from django.template import loader
from django.db.models import Count
from .models import Commodities

import json

def home(request):
   template = loader.get_template('home.html')
   return HttpResponse(template.render())

def market(request):
   # Get the number of auctions per timestamp
   auction_counts = Commodities.objects.values('timestamp').annotate(num_auctions = Count('id')).order_by('timestamp')
   count_list = [auction_count['num_auctions'] for auction_count in auction_counts]
   # Get a list of timestamps
   timestamp_list = [str(auction_count['timestamp']) for auction_count in auction_counts]
   # Set up template data
   template = loader.get_template('market.html')
   context = {'timestamp_list': json.dumps(timestamp_list), 'auctions_count_list': json.dumps(count_list)}
   return HttpResponse(template.render(context, request))

def distribution(request):
   # Get items grouped by quality
   quantities = Commodities.objects.values('quality').annotate(total_quantity = Count('quantity')).order_by('-total_quantity')
   # Get items grouped by level
   level = Commodities.objects.values('level').annotate(total_level = Count('level'))
   # Set up template data
   template = loader.get_template('distribution.html')
   context = {'quantities': json.dumps(list(quantities)), 'level':json.dumps(list(level))}
   return HttpResponse(template.render(context, request))

def profit(request):
   template = loader.get_template('profit.html')
   return HttpResponse(template.render())

def data(request):
   template = loader.get_template('data.html')
   return HttpResponse(template.render())
