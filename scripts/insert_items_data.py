from core.models import ItemsData
import csv

# Insert data into table ItemsData
def run():
   with open('data/items_data.csv') as file:
      data = csv.DictReader(file)
      ItemsData.objects.all().delete()
      count = 0
      objects = []
      for row in data:
         count += 1
         print(count, row)
         item_data = ItemsData(**row)
         objects.append(item_data)
      ItemsData.objects.bulk_create(objects)
