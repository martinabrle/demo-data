import pandas as pd
import simplejson as json

# Read CSV files
customers_df = pd.read_csv('../Customers.csv', names=['customerId','emailAddress','phoneNumber','faxNumber','webAddress','addressId','name','legalForm','createdBy','createdDateTime','modifiedBy','modifiedDateTime','currency'], dtype={'createdBy': 'str', 'modifiedBy': 'str', 'customerId': 'str', 'addressId': 'str', 'createdDateTime': 'str', 'modifiedDateTime': 'str'}, skiprows=1)
customers_df.insert(1,'entityType', 'Customer')
addresses_df = pd.read_csv('../Addresses.csv', names=['addressId','city','postalCode','street','building','country','region','addressType','validityStartDateTime','validityEndDateTime','latitude','longitude'], dtype={'createdBy': 'str', 'modifiedBy': 'str', 'addressId': 'str', 'building': 'str', 'validityStartDateTime': 'str','validityEndDateTime': 'str'}, skiprows=1)
addresses_df.insert(0,'entityType', 'Address')
employees_df = pd.read_csv('../Employees.csv', names=['employeeId','firstName','middleName','lastName','initials','sex','language','phoneNumber','emailAddress','loginName','addressId','validFromDateTime','validaToDateTime'], dtype={'createdBy': 'str', 'modifiedBy': 'str', 'employeeId': 'str', 'addressId': 'str'}, skiprows=1)
employees_filtered_df = employees_df[['employeeId', 'firstName', 'lastName', 'middleName', 'emailAddress', 'loginName']]
employees_filtered_df.insert(0,'entityType', 'Employee')

employees_filtered_dict = employees_filtered_df.set_index('employeeId').to_dict(orient='index')

# Merge Employees into Customers
customers_df['createdByEmpl'] = customers_df['createdBy'].map(employees_filtered_dict)
customers_df['modifiedByEmpl'] = customers_df['modifiedBy'].map(employees_filtered_dict)

# Merge Addresses into Customers
addresses_dict = addresses_df.set_index('addressId').to_dict(orient='index')
customers_df['address'] = customers_df['addressId'].map(addresses_dict)

# Convert to list of dictionaries
json_list = customers_df.to_dict(orient='records')

# Write to JSON file
with open('customers.json', 'w') as json_file:
    json.dump(json_list, json_file, indent=4, ignore_nan=True)