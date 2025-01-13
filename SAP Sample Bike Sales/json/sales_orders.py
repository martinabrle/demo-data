import pandas as pd
import simplejson as json

# Read CSV files
sales_orders_df = pd.read_csv('salesOrders.csv', dtype={'createdBy': 'str', 'modifiedBy': 'str', 'customerId': 'str', 'salesOrderId': 'str'})
sales_order_items_df = pd.read_csv('salesOrderItems.csv', dtype={'createdBy': 'str', 'modifiedBy': 'str', 'customerId': 'str', 'salesOrderId': 'str'})
customers_df = pd.read_csv('customers.csv', dtype={'createdBy': 'str', 'modifiedBy': 'str', 'customerId': 'str', 'addressId': 'str'})
addresses_df = pd.read_csv('addresses.csv', dtype={'createdBy': 'str', 'modifiedBy': 'str', 'addressId': 'str'})
employees_df = pd.read_csv('employees.csv', dtype={'createdBy': 'str', 'modifiedBy': 'str', 'employeeId': 'str', 'addressId': 'str'})
employees_filtered_df = employees_df[['employeeId', 'firstName', 'lastName', 'middleName', 'emailAddress', 'loginName']]
products_df = pd.read_csv('products.csv', dtype={'createdBy': 'str', 'modifiedBy': 'str', 'vendorId': 'str', 'taxTariffCode': 'str', 'width': 'str', 'height': 'str', 'depth': 'str', 'dimensionUnit': 'str', 'productPicUrl': 'str'})
product_texts_df = pd.read_csv('productTexts.csv')

# Convert product texts to dictionary grouped by productId
product_texts_grouped = product_texts_df.groupby('productId').apply(lambda x: x.to_dict(orient='records')).to_dict()

# Merge product texts into products
products_df['texts'] = products_df['productId'].map(product_texts_grouped)

employees_filtered_dict = employees_filtered_df.set_index('employeeId').to_dict(orient='index')

# Merge Products into Sales Order Lines
products_df = products_df.set_index('productId').to_dict(orient='index')

sales_order_items_df['product'] = sales_order_items_df['productId'].map(products_df)

# Convert Sales Order Items to dictionary grouped by salesOrderId
sales_order_items_grouped = sales_order_items_df.groupby('salesOrderId').apply(lambda x: x.to_dict(orient='records')).to_dict()

# Merge Employees into Sales Orders
sales_orders_df['createdByEmpl'] = sales_orders_df['createdBy'].map(employees_filtered_dict)
sales_orders_df['modifiedByEmpl'] = sales_orders_df['modifiedBy'].map(employees_filtered_dict)

# Merge Employees into Customers
customers_df['createdByEmpl'] = customers_df['createdBy'].map(employees_filtered_dict)
customers_df['modifiedByEmpl'] = customers_df['modifiedBy'].map(employees_filtered_dict)

# Merge Customers into Sales Orders
customers_dict = customers_df.set_index('customerId').to_dict(orient='index')
sales_orders_df['customer'] = sales_orders_df['customerId'].map(customers_dict)

# Merge Sales Order Lines into Sales Orders
sales_orders_df['orderLines'] = sales_orders_df['salesOrderId'].map(sales_order_items_grouped)

# Merge Addresses into Customers
addresses_dict = addresses_df.set_index('addressId').to_dict(orient='index')
customers_df['address'] = customers_df['addressId'].map(addresses_dict)

# Convert to list of dictionaries
json_list = sales_orders_df.to_dict(orient='records')

# Write to JSON file
with open('salesOrders.json', 'w') as json_file:
    json.dump(json_list, json_file, indent=4, ignore_nan=True)