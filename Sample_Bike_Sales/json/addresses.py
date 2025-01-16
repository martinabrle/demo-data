import pandas as pd
import simplejson as json

# Read CSV files
addresses_df = pd.read_csv('../Addresses.csv', names=['addressId','city','postalCode','street','building','country','region','addressType','validityStartDateTime','validityEndDateTime','latitude','longitude'], dtype={'createdBy': 'str', 'modifiedBy': 'str', 'addressId': 'str', 'building': 'str', 'validityStartDateTime': 'str', 'validityEndDateTime': 'str'}, skiprows=1)
addresses_df.insert(1,'entityType', 'Address')

addresses_dict = addresses_df.set_index('addressId').to_dict(orient='index')

json_list = addresses_df.to_dict(orient='records')

# Write to JSON file
with open('addresses.json', 'w') as json_file:
    json.dump(json_list, json_file, indent=4, ignore_nan=True)