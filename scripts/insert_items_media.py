from core.models import ItemsMedia
import csv

# Insert data into table ItemsMedia
def run():
   with open('data/items_media.csv') as file:
      data = csv.DictReader(file)
      ItemsMedia.objects.all().delete()
      count = 0
      objects = []
      for row in data:
         count += 1
         print(count, row)
         item_media = ItemsMedia(**row)
         objects.append(item_media)
      ItemsMedia.objects.bulk_create(objects)
