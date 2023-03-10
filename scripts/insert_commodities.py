from core.models import Commodities
import csv

# Insert data into table Commodities
def run():
   with open('data/commodities.csv') as file:
      data = csv.DictReader(file)
      Commodities.objects.all().delete()
      count = 0
      objects = []
      for row in data:
         count += 1
         print(count, row)
         commodity = Commodities(**row)
         objects.append(commodity)
         if count % 100000 == 0:
            Commodities.objects.bulk_create(objects)
            objects = []
      Commodities.objects.bulk_create(objects)
