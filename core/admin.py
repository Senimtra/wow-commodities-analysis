from django.contrib import admin
from .models import Commodities, Auctions, ItemsData, ItemsMedia

class CommoditiesAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'quantity', 'unit_price', 'weighted', 'timestamp')

class AuctionsAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'quantity', 'unit_price', 'timestamp')

class ItemsDataAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'name', 'quality', 'level', 'item_class', 'item_subclass', 'description')

class ItemsMediaAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'media', 'link')

admin.site.register(Commodities, CommoditiesAdmin)
admin.site.register(Auctions, AuctionsAdmin)
admin.site.register(ItemsData, ItemsDataAdmin)
admin.site.register(ItemsMedia, ItemsMediaAdmin)
