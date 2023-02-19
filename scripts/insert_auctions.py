from core.models import Auctions
import csv

# Insert data into table Auctions
def run():
   with open('data/auctions.csv') as file:
      data = csv.DictReader(file)
      Auctions.objects.all().delete()
      count = 0
      objects = []
      for row in data:
         count += 1
         print(count, row)
         auction = Auctions(**row)
         objects.append(auction)
      Auctions.objects.bulk_create(objects)
