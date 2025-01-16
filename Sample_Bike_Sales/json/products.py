import pandas as pd
import simplejson as json

# Read CSV files
products_df = pd.read_csv('../Products.csv', names=['productId','typeCode','prodCategoryId','createdBy','createdDateTime','modifiedBy','modifiedDateTime','vendorId','taxTariffCode','quantityUnit','weightMeasure','weightUnit','currency','price','width','depth','height','dimensionUnit','productPicUrl'], dtype={'createdBy': 'str', 'modifiedBy': 'str', 'vendorId': 'str', 'taxTariffCode': 'str', 'width': 'str', 'height': 'str', 'depth': 'str', 'dimensionUnit': 'str', 'productPicUrl': 'str'}, skiprows=1)
products_df.insert(1,'entityType', 'Product')
product_texts_df = pd.read_csv('../ProductTexts.csv', names=['productId','language','shortDescription','mediumDescription','longDescription'], skiprows=1)
product_texts_df.insert(0,'entityType', 'ProductText')
employees_df = pd.read_csv('../Employees.csv', names=['employeeId','firstName','middleName','lastName','initials','sex','language','phoneNumber','emailAddress','loginName','addressId','validFromDateTime','validToDateTime'], dtype={'createdBy': 'str', 'modifiedBy': 'str', 'employeeId': 'str', 'addressId': 'str', 'validFromDateTime': 'str', 'validToDateTime': 'str'}, skiprows=1)
employees_filtered_df = employees_df[['employeeId', 'firstName', 'lastName', 'middleName', 'emailAddress', 'loginName']]
employees_filtered_df.insert(0,'entityType', 'Employee')

employees_filtered_dict = employees_filtered_df.set_index('employeeId').to_dict(orient='index')

# Merge Employees into Vendors
products_df['createdByEmpl'] = products_df['createdBy'].map(employees_filtered_dict)
products_df['modifiedByEmpl'] = products_df['modifiedBy'].map(employees_filtered_dict)

# Convert product texts to dictionary grouped by productId
product_texts_grouped = product_texts_df.groupby('productId').apply(lambda x: x.to_dict(orient='records')).to_dict()

# Merge product texts into products
products_df['texts'] = products_df['productId'].map(product_texts_grouped)

# Convert to list of dictionaries
json_list = products_df.to_dict(orient='records')

# Write to JSON file
with open('products.json', 'w') as json_file:
    json.dump(json_list, json_file, indent=4, ignore_nan=True)