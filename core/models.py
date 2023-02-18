from django.db import models

# Commodities database model
class Commodities(models.Model):
   item_id = models.IntegerField()
   quantity = models.IntegerField()
   unit_price = models.IntegerField()
   weighted = models.IntegerField()
   timestamp = models.DateTimeField()

# Auctions database model
class Auctions(models.Model):
   item_id = models.IntegerField()
   quantity = models.IntegerField()
   unit_price = models.IntegerField()
   timestamp = models.DateTimeField()
