# Imports
import pandas as pd
import numpy as np
import requests
import re
from datetime import datetime

# Read credentials
with open('./api_credentials.txt', 'r') as file:
   text = file.read()   
credentials = re.findall('=(.*)', text)

# Assign credentials
client_ID = credentials[0]
client_secret = credentials[1]

# Create access token
def create_access_token(client_ID, client_secret, region = 'eu'):
   data = {'grant_type': 'client_credentials'}
   response = requests.post('https://%s.battle.net/oauth/token' % region, data = data, auth = (client_ID, client_secret))
   return response.json()

response = create_access_token(client_ID, client_secret)
access_token = response['access_token']

# Get commodity auctions data
def get_commodities(access_token):
   search = f'https://eu.api.blizzard.com/data/wow/auctions/commodities?namespace=dynamic-eu&locale=en_GB&access_token={access_token}'
   response = requests.get(search)
   return response.json()['auctions']

commodities_data = get_commodities(access_token)
commodities_df = pd.DataFrame(commodities_data)

# Get EU-Ravencrest auctions data
def get_ravencrest(access_token):
   search = f'https://eu.api.blizzard.com/data/wow/connected-realm/1329/auctions?namespace=dynamic-eu&locale=en_GB&access_token={access_token}'
   response = requests.get(search)
   return response.json()['auctions']

auctions_data = get_ravencrest(access_token)
auctions_df = pd.DataFrame(auctions_data)

# Remove items that do not have a buyout price
auctions_df = auctions_df[~auctions_df['buyout'].isna()]

# Remove items that have a price higher than gold limit (9999999g)
auctions_df = auctions_df[auctions_df['buyout'] < 1000000000]

# Add timestamp
now = datetime.now()
date_str = now.strftime('%Y-%m-%d %H:%M:%S')

commodities_df['timestamp'] = date_str
commodities_df['timestamp'] = pd.to_datetime(commodities_df['timestamp'])

auctions_df['timestamp'] = date_str
auctions_df['timestamp'] = pd.to_datetime(auctions_df['timestamp'])

# Extract item ids
commodities_df['item'] = commodities_df['item'].apply(lambda x: x['id'])
auctions_df['item'] = auctions_df['item'].apply(lambda x: x['id'])

# Rename columns
commodities_df.rename(columns = {'id': 'auction_id', 'item': 'item_id'}, inplace = True)
auctions_df.rename(columns = {'id': 'auction_id', 'item': 'item_id'}, inplace = True)

# Drop columns 'auction_id' + 'time_left'
commodities_df.drop(['auction_id', 'time_left'], axis = 1, inplace = True)

# Drop columns 'auction_id', 'time_left', 'bid'
auctions_df.drop(['auction_id', 'time_left', 'bid'], axis = 1, inplace = True)

# Use the weighted (quantity) median to pick a reasonable unit price
def weighted_median(item_df):
   sorted_df = item_df.sort_values('unit_price') # sort values in ascending order by unit_price
   cum_weights = sorted_df['quantity'].cumsum() # calculate the cumulative sum of quantities
   total_weight = cum_weights.iloc[-1] # get the total weight
   if total_weight % 2 == 1: # if the total weight is odd
      median_index = cum_weights.searchsorted(total_weight / 2) # find the index of the median
      return sorted_df.iloc[median_index]['unit_price'] # return the corresponding unit_price value
   else: # if the total weight is even
      median_index = cum_weights.searchsorted(total_weight / 2, side = 'right') # find the index of the right median
      median_values = sorted_df.iloc[median_index - 1: median_index]['unit_price'] # get the two median values
      # If the mean of the two median values is NaN, return the median unit price (unweighted)
      return item_df['unit_price'].median() if pd.isna(median_values.mean()) else median_values.mean()
   
price_weighted_median = commodities_df.groupby('item_id').apply(lambda x: weighted_median(x)).reset_index(name = 'weighted')
price_weighted_median['weighted'] = price_weighted_median['weighted'].astype('int64')

# Group by item_id and sum quantity
commodities_df = commodities_df.groupby('item_id').agg({'unit_price': np.min, 'timestamp': 'first', 'quantity': np.sum})

# Merge commodities + weighted median price
commodities_df = pd.merge(commodities_df, price_weighted_median, left_on = 'item_id', right_on = 'item_id')
commodities_df = commodities_df[['item_id', 'quantity', 'unit_price', 'weighted', 'timestamp']]

# Use the cheapest price available since there is no way to get information about the sold auctions.
auctions_df = auctions_df.groupby('item_id').agg({'buyout': np.min, 'quantity': np.sum, 'timestamp': 'first'})
auctions_df.reset_index(inplace = True)

auctions_df['buyout'] = auctions_df['buyout'].astype(int)
auctions_df.rename(columns = {'buyout': 'unit_price'}, inplace = True)
auctions_df = auctions_df[['item_id', 'quantity', 'unit_price', 'timestamp']]

# Save commodities data to file
def stamp_string(timestamp):
   day = re.findall('-(\d.) ', str(timestamp))[0]
   hour = re.findall(' (\d.):', str(timestamp))[0]
   return 'd' + day + '_h' + hour

file_stamp_commodities = stamp_string(commodities_df.iloc[:1, 4])
commodities_df.to_csv(f'./data/commodities/{file_stamp_commodities}_commodities.csv', index = False, date_format = '%Y-%m-%d %H:%M:%S')

file_stamp_auctions = stamp_string(auctions_df.iloc[:1, 3])
auctions_df.to_csv(f'./data/auctions/{file_stamp_auctions}_auctions.csv', index = False, date_format = '%Y-%m-%d %H:%M:%S')
