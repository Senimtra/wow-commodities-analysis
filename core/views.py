# Imports
from django.http import HttpResponse
from django.template import loader
from django.db.models import Count, Sum, F, Window, Max, Min
from django.db.models.functions import Rank
from .models import Commodities, Auctions
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
   # Get the total market revenue
   revenue_counts = Auctions.objects.values('timestamp').annotate(count_revenues = Sum(F('quantity') * F('unit_price'))).order_by('timestamp')
   revenue_counts_list = [revenue_count['count_revenues'] for revenue_count in revenue_counts]
   # Get a list of timestamps
   timestamp_list = [str(item_count['timestamp']) for item_count in item_counts]
   # Set up template data
   template = loader.get_template('market.html')
   context = {'timestamp_list': json.dumps(timestamp_list), 'item_counts_list': json.dumps(item_counts_list), 'quantity_counts_list': json.dumps(quantity_counts_list), 'revenue_counts_list': revenue_counts_list}
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

   items_ranked_quantity = (Commodities.objects.values('item_id', 'link', 'name').annotate(total_quantity = Sum('quantity')).order_by('-total_quantity')
    .annotate(rank = Window(expression = Rank(), order_by = F('total_quantity').desc())))
   items_ranked_pricerange = Commodities.objects.values('item_id').annotate(price_diff = Max('unit_price') - Min('unit_price')).order_by('-price_diff')
   items_ranked_pricerange = items_ranked_pricerange.annotate(rank = Window(expression = Rank(), order_by = F ('price_diff').desc()))

   for item_id1 in items_ranked_quantity:
      for item_id2 in items_ranked_pricerange:
         if item_id1['item_id'] == item_id2['item_id']:
            item_id1['price_range'] = item_id2['price_diff']
            item_id1['rank'] += item_id2['rank']
            break
   
   items_ranked = sorted(items_ranked_quantity, key = lambda x: x['rank'])[:25]

   for item in items_ranked:
      item_id = item['item_id']
      item_prices = Commodities.objects.filter(item_id = item_id).order_by('unit_price')
      item['timestamp_min'] = item_prices[0].timestamp.strftime('%A %H')
      item['timestamp_max'] = item_prices.reverse()[0].timestamp.strftime('%A %H')

   template = loader.get_template('profit.html')
   context = {'items_ranked': items_ranked}
   return HttpResponse(template.render(context, request))

def data(request):
   template = loader.get_template('data.html')
   return HttpResponse(template.render())
