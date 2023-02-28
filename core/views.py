from django.http import HttpResponse
from django.template import loader
from django.db.models import Count, Sum
from .models import Commodities

import json

def home(request):
   template = loader.get_template('home.html')
   return HttpResponse(template.render())

def market(request):
   # Get the number of unique items per timestamp
   item_counts = Commodities.objects.values('timestamp').annotate(count_items = Count('id')).order_by('timestamp')
   item_counts_list = [item_count['count_items'] for item_count in item_counts]
   # Get the number of traded quantities
   quantity_counts = Commodities.objects.values('timestamp').annotate(count_quantities = Sum('quantity')).order_by('timestamp')
   quantity_counts_list = [quantity_count['count_quantities'] for quantity_count in quantity_counts]
   # Get a list of timestamps
   timestamp_list = [str(item_count['timestamp']) for item_count in item_counts]
   # Set up template data
   template = loader.get_template('market.html')
   context = {'timestamp_list': json.dumps(timestamp_list), 'item_counts_list': json.dumps(item_counts_list), 'quantity_counts_list': json.dumps(quantity_counts_list)}
   return HttpResponse(template.render(context, request))

def distribution(request):
   # Get items grouped by quality
   quantities = Commodities.objects.values('quality').annotate(total_quantity = Count('quality')).order_by('-total_quantity')
   # Get items grouped by level
   level = Commodities.objects.values('level').annotate(total_quantity = Count('level'))
   # Get items grouped by class
   item_class = Commodities.objects.values('item_class').annotate(total_quantity = Count('item_class')).order_by('-total_quantity')
   # Get items grouped by subclass
   item_subclass = Commodities.objects.values('item_subclass').annotate(total_quantity = Count('item_subclass'))
   # Set up template data
   template = loader.get_template('distribution.html')
   context = {'quantities': json.dumps(list(quantities)), 'level': json.dumps(list(level)), 'class': json.dumps(list(item_class)), 'subclass': json.dumps(list(item_subclass))}
   return HttpResponse(template.render(context, request))

def profit(request):
   template = loader.get_template('profit.html')
   return HttpResponse(template.render())

def data(request):
   template = loader.get_template('data.html')
   return HttpResponse(template.render())
