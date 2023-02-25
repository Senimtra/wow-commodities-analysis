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

# Items data table model
class ItemsData(models.Model):
   item_id = models.IntegerField()
   name = models.CharField(max_length = 100)
   quality = models.CharField(max_length = 20)
   level = models.IntegerField()
   item_class = models.CharField(max_length = 30)
   item_subclass = models.CharField(max_length = 30)
   description = models.TextField(max_length = 500)

# Items media table model
class ItemsMedia(models.Model):
   item_id = models.IntegerField()
   media = models.CharField(max_length = 20)
   link = models.CharField(max_length = 255)
