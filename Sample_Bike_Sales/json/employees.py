import pandas as pd
import simplejson as json

# Read CSV files
employees_df = pd.read_csv('../Employees.csv', names=['employeeId','firstName','middleName','lastName','initials','sex','language','phoneNumber','emailAddress','loginName','addressId','validFromDateTime','validToDateTime'], dtype={'createdBy': 'str', 'modifiedBy': 'str', 'employeeId': 'str', 'addressId': 'str', 'validFromDateTime': 'str', 'validToDateTime': 'str'}, skiprows=1)
employees_df.insert(1,'entityType', 'Employee')
addresses_df = pd.read_csv('../Addresses.csv', names=['addressId','city','postalCode','street','building','country','region','addressType','validityStartDateTime','validityEndDateTime','latitude','longitude'], dtype={'createdBy': 'str', 'modifiedBy': 'str', 'addressId': 'str', 'building': 'str', 'validityStartDateTime': 'str','validityEndDateTime': 'str'}, skiprows=1)
addresses_df.insert(0,'entityType', 'Address')
addresses_dict = addresses_df.set_index('addressId').to_dict(orient='index')
employees_df['address'] = employees_df['addressId'].map(addresses_dict)

json_list = employees_df.to_dict(orient='records')

# Write to JSON file
with open('employees.json', 'w') as json_file:
    json.dump(json_list, json_file, indent=4, ignore_nan=True)