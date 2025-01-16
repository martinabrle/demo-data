import pandas as pd
import simplejson as json

# Read CSV files
sales_order_items_df = pd.read_csv('../SalesOrderItems.csv', names=['salesOrderId','salesOrderItemId','productId','note','currency','grossAmount','netAmount','taxAmount','itemATPStatus','opItemPos','quantity','quantityUnit','deliveryDate'], dtype={'createdBy': 'str', 'modifiedBy': 'str', 'customerId': 'str', 'salesOrderId': 'str', 'deliveryDate': 'str'}, skiprows=1)
sales_order_items_df.insert(1,'entityType', 'SalesOrderItem')
employees_df = pd.read_csv('../Employees.csv', names=['employeeId','firstName','middleName','lastName','initials','sex','language','phoneNumber','emailAddress','loginName','addressId','validFromDateTime','validaToDateTime'], dtype={'createdBy': 'str', 'modifiedBy': 'str', 'employeeId': 'str', 'addressId': 'str'}, skiprows=1)
employees_filtered_df = employees_df[['employeeId', 'firstName', 'lastName', 'middleName', 'emailAddress', 'loginName']]
employees_filtered_df.insert(0,'entityType', 'Employee')
products_df = pd.read_csv('../Products.csv', names=['productId','typeCode','productCategoryId','createdBy','createdDateTime','modifiedBy','modifiedDateTime','vendorId','taxTariffCode','quantityUnit','weightMeasure','weightUnit','currency','price','width','depth','height','dimensionUnit','productPicUrl'], dtype={'createdBy': 'str', 'modifiedBy': 'str', 'vendorId': 'str', 'taxTariffCode': 'str', 'width': 'str', 'height': 'str', 'depth': 'str', 'dimensionUnit': 'str', 'productPicUrl': 'str', 'createdDateTime': 'str', 'modifiedDateTime': 'str'}, skiprows=1)
products_df.insert(0,'entityType', 'Product')
product_texts_df = pd.read_csv('../ProductTexts.csv', names=['productId','language','shortDescription','mediumDescription','longDescription'], skiprows=1)
product_texts_df.insert(0,'entityType', 'ProductText')
vendors_df = pd.read_csv('../Vendors.csv', names=['vendorId','emailAddress','phoneNumber','faxNumber','webAddress','addressId','name','legalForm','createdBy','createdDateTime','modifiedBy','modifiedDateTime','currency'], dtype={'createdBy': 'str', 'modifiedBy': 'str', 'vendorId': 'str', 'addressId': 'str', 'createdDateTime': 'str', 'modifiedDateTime': 'str', 'phoneNumber': 'str', 'faxNumber': 'str'}, skiprows=1)
vendors_df.insert(0,'entityType', 'Vendor')

# Convert product texts to dictionary grouped by productId
product_texts_grouped = product_texts_df.groupby('productId',).apply(lambda x: x.to_dict(orient='records')).to_dict()

# Merge product texts into products
products_df['texts'] = products_df['productId'].map(product_texts_grouped)

employees_filtered_dict = employees_filtered_df.set_index('employeeId').to_dict(orient='index')

# Merge Employees into Vendors
vendors_df['createdByEmpl'] = vendors_df['createdBy'].map(employees_filtered_dict)
vendors_df['modifiedByEmpl'] = vendors_df['modifiedBy'].map(employees_filtered_dict)

# Merge Vendors into Products
products_df['vendor'] = products_df['vendorId'].map(vendors_df.set_index('vendorId').to_dict(orient='index'))

# Merge Products into Sales Order Lines
products_df = products_df.set_index('productId').to_dict(orient='index')

sales_order_items_df['product'] = sales_order_items_df['productId'].map(products_df)

# Convert to list of dictionaries
json_list = sales_order_items_df.to_dict(orient='records')

# Write to JSON file
with open('salesOrderItems.json', 'w') as json_file:
    json.dump(json_list, json_file, indent=4, ignore_nan=True)