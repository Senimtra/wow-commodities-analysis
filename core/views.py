# Imports
from django.http import HttpResponse
from django.template import loader
from django.db.models import Count, Sum, F, Avg, Window, Max, Min
from django.db.models.functions import Rank
from django.db import connection
from scipy.signal import savgol_filter
from functions import database
from .models import Commodities, Auctions
import json
import re

def home(request):
   template = loader.get_template('home.html')
   return HttpResponse(template.render())

def analysis(request):
   template = loader.get_template('analysis.html')
   return HttpResponse(template.render())

def market(request):
   # Get the number of unique items per timestamp
   item_counts = Commodities.objects.values('timestamp').annotate(count_items = Count('id')).order_by('timestamp')
   item_counts_list = [item_count['count_items'] for item_count in item_counts]
   # Get the number of traded quantities
   quantity_counts = Commodities.objects.values('timestamp').annotate(count_quantities = Sum('quantity')).order_by('timestamp')
   quantity_counts_list = [quantity_count['count_quantities'] for quantity_count in quantity_counts]
   # Get the total market revenue
   revenue_counts = Auctions.objects.values('timestamp').annotate(count_revenues = Sum(F('quantity') * F('unit_price')) / 10000).order_by('timestamp')
   revenue_counts_list = [revenue_count['count_revenues'] / 100 for revenue_count in revenue_counts]
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
   # Rank items by their traded quantity
   items_ranked_quantity = (Commodities.objects.exclude(item_subclass='Junk').values('item_id', 'link', 'name').annotate(total_quantity = Sum('quantity') / 168).order_by('-total_quantity')
    .annotate(rank = Window(expression = Rank(), order_by = F('total_quantity').desc())))
   # Rank items by their price range
   items_ranked_pricerange = Commodities.objects.exclude(item_subclass='Junk').values('item_id').annotate(profit = (Max('unit_price') - Min('unit_price')) / 100).order_by('-profit')
   items_ranked_pricerange = items_ranked_pricerange.annotate(rank = Window(expression = Rank(), order_by = F ('profit').desc()))
   # Combine ranks and items data
   for item_id1 in items_ranked_quantity:
      for item_id2 in items_ranked_pricerange:
         if item_id1['item_id'] == item_id2['item_id']:
            item_id1['profit'] = item_id2['profit']
            item_id1['rank'] += item_id2['rank']
            break
   # Sort items by their combined rank (quantities, pricerange)
   items_ranked = sorted(items_ranked_quantity, key = lambda x: x['rank'])[:102]
   # Set up template data
   template = loader.get_template('profit.html')
   context = {'items_ranked': items_ranked}
   return HttpResponse(template.render(context, request))

def details(request, item_id):
   # Get item data from profit view
   link = request.POST.get('link')
   name = request.POST.get('name')
   quantity = request.POST.get('quantity')
   rank = request.POST.get('rank')
   comb_rank = request.POST.get('comb_rank')
   profit = request.POST.get('profit')
   # Get missing item data
   enriched = Commodities.objects.filter(item_id = item_id).annotate(avg_price = Avg('unit_price') / 100).values('item_id', 'quantity', 'unit_price', 'timestamp', 'name', 'quality', 'level', 'item_class', 'item_subclass', 'description', 'media', 'link', 'avg_price').first()
   # Set up template data (missing data)
   avg_price = int(enriched['avg_price'])
   quality = enriched['quality']
   level = enriched['level']
   item_class = enriched['item_class']
   item_subclass = enriched['item_subclass']
   description = enriched['description']
   # Set up template data (chart: prices + days)
   chart = Commodities.objects.filter(item_id = item_id).values('unit_price', 'timestamp').order_by('timestamp')
   chart_prices = savgol_filter([int(obj['unit_price'] / 100) for obj in chart], window_length = 12, polyorder = 2)
   chart_timestamps = [obj['timestamp'].strftime('%A %H') for obj in chart]
   # Set up template data (buy sell points)
   buy_sell_point = list(zip(chart_prices, chart_timestamps))
   buy_point = f'{min(buy_sell_point, key=lambda x: x[0])[1]}:00'
   sell_point = f'{max(buy_sell_point, key=lambda x: x[0])[1]}:00'
   # Set up template data object
   template = loader.get_template('details.html')
   context = {'item_id': item_id, 'link': link, 'name': name, 'quantity': quantity, 'rank': rank, 'comb_rank': comb_rank, 'profit': profit, 'avg_price': avg_price, 'quality': quality, 'level': level, 'item_class': item_class, 'item_subclass': item_subclass, 'description': description, 'buy_point': buy_point, 'sell_point': sell_point, 'chart_timestamps': json.dumps(chart_timestamps), 'chart_prices': json.dumps(list(chart_prices))}
   return HttpResponse(template.render(context, request))

def data(request):
   # Get database table names + number of rows
   with connection.cursor() as cursor:
      cursor.execute("SELECT relname, n_live_tup FROM pg_stat_user_tables ORDER BY n_live_tup DESC")
      results = cursor.fetchall()
   tables_rows = [(result[0][5:], result[1]) for result in results if 'core_' in result[0]]
   total_rows = '.'.join(re.findall(r'\d{1,3}(?=(?:\d{3})+$)|\d{1,3}$', str(sum([rows[1] for rows in tables_rows]))))
   # Set up template data
   template = loader.get_template('data.html')
   context = {'database_status': database.status(), 'tables_rows': tables_rows, 'total_rows': total_rows}
   return HttpResponse(template.render(context, request))
