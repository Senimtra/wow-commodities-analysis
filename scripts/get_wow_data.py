# Imports
import pandas as pd
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

ravencrest_data = get_ravencrest(access_token)
ravencrest_df = pd.DataFrame(ravencrest_data)

# Add timestamp
now = datetime.now()
date_str = now.strftime('%Y-%m-%d %H:%M:%S')

commodities_df['timestamp'] = date_str
commodities_df['timestamp'] = pd.to_datetime(commodities_df['timestamp'])

ravencrest_df['timestamp'] = date_str
ravencrest_df['timestamp'] = pd.to_datetime(ravencrest_df['timestamp'])

# Extract item ids
commodities_df['item'] = commodities_df['item'].apply(lambda x: x['id'])
ravencrest_df['item'] = ravencrest_df['item'].apply(lambda x: x['id'])

# Rename columns
commodities_df.rename(columns = {'id': 'auction_id', 'item': 'item_id'}, inplace = True)
ravencrest_df.rename(columns = {'id': 'auction_id', 'item': 'item_id'}, inplace = True)

# Save commodities data to file
def stamp_string(timestamp):
   day = re.findall('-(\d.) ', str(timestamp))[0]
   hour = re.findall(' (\d.):', str(timestamp))[0]
   return 'd' + day + '_h' + hour

file_stamp_commodities = stamp_string(commodities_df.iloc[:1, 5])
commodities_df.to_csv(f'./data/commodities/{file_stamp_commodities}_commodities.csv')

file_stamp_ravencrest = stamp_string(ravencrest_df.iloc[:1, 6])
ravencrest_df.to_csv(f'./data/auctions/{file_stamp_ravencrest}_auctions.csv')
