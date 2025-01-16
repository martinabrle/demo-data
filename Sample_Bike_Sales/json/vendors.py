import pandas as pd
import simplejson as json

# Read CSV files
vendors_df = pd.read_csv('../Vendors.csv', names=['vendorId','emailAddress','phoneNumber','faxNumber','webAddress','addressId','name','legalForm','createdBy','createdDateTime','modifiedBy','modifiedDateTime','currency'], dtype={'createdBy': 'str', 'modifiedBy': 'str', 'vendorId': 'str', 'addressId': 'str', 'createdDateTime': 'str', 'modifiedDateTime': 'str', 'phoneNumber': 'str', 'faxNumber': 'str'}, skiprows=1)
vendors_df.insert(1,'entityType', 'Vendor')
addresses_df = pd.read_csv('../Addresses.csv', names=['addressId','city','postalCode','street','building','country','region','addressType','validityStartDateTime','validityEndDateTime','latitude','longitude'], dtype={'createdBy': 'str', 'modifiedBy': 'str', 'addressId': 'str', 'building': 'str', 'validityStartDateTime': 'str','validityEndDateTime': 'str'}, skiprows=1)
addresses_df.insert(0,'entityType', 'Address')
employees_df = pd.read_csv('../Employees.csv', names=['employeeId','firstName','middleName','lastName','initials','sex','language','phoneNumber','emailAddress','loginName','addressId','validFromDateTime','validaToDateTime'], dtype={'createdBy': 'str', 'modifiedBy': 'str', 'employeeId': 'str', 'addressId': 'str'}, skiprows=1)
employees_filtered_df = employees_df[['employeeId', 'firstName', 'lastName', 'middleName', 'emailAddress', 'loginName']]
employees_filtered_df.insert(0,'entityType', 'Employee')

employees_filtered_dict = employees_filtered_df.set_index('employeeId').to_dict(orient='index')

# Merge Employees into Vendors
vendors_df['createdByEmpl'] = vendors_df['createdBy'].map(employees_filtered_dict)
vendors_df['modifiedByEmpl'] = vendors_df['modifiedBy'].map(employees_filtered_dict)

# Merge Addresses into Vendors
addresses_dict = addresses_df.set_index('addressId').to_dict(orient='index')
vendors_df['address'] = vendors_df['addressId'].map(addresses_dict)

# Convert to list of dictionaries
json_list = vendors_df.to_dict(orient='records')

# Write to JSON file
with open('vendors.json', 'w') as json_file:
    json.dump(json_list, json_file, indent=4, ignore_nan=True)