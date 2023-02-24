from django.db import models

# Commodities table model
class Commodities(models.Model):
   item_id = models.IntegerField()
   quantity = models.IntegerField()
   unit_price = models.IntegerField()
   weighted = models.IntegerField()
   timestamp = models.DateTimeField()

   class Meta:
      verbose_name_plural = 'commodities'

# Auctions table model
class Auctions(models.Model):
   item_id = models.IntegerField()
   quantity = models.IntegerField()
   unit_price = models.IntegerField()
   timestamp = models.DateTimeField()

   class Meta:
      verbose_name_plural = 'auctions'
