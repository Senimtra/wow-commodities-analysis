from django.contrib import admin
from .models import Commodities, Auctions

class CommoditiesAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'quantity', 'unit_price', 'weighted', 'timestamp')

class AuctionsAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'quantity', 'unit_price', 'timestamp')

admin.site.register(Commodities, CommoditiesAdmin)
admin.site.register(Auctions, AuctionsAdmin)
