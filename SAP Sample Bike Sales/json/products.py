import pandas as pd
import simplejson as json

# Read CSV files
products_df = pd.read_csv('json/products.csv', dtype={'createdBy': 'str', 'modifiedBy': 'str', 'vendorId': 'str', 'taxTariffCode': 'str', 'width': 'str', 'height': 'str', 'depth': 'str', 'dimensionUnit': 'str', 'productPicUrl': 'str'})
product_texts_df = pd.read_csv('json/productTexts.csv')

# Convert product texts to dictionary grouped by productId
product_texts_grouped = product_texts_df.groupby('productId').apply(lambda x: x.to_dict(orient='records')).to_dict()

# Merge product texts into products
products_df['texts'] = products_df['productId'].map(product_texts_grouped)

# Convert to list of dictionaries
json_list = products_df.to_dict(orient='records')

# Write to JSON file
with open('json/products.json', 'w') as json_file:
    json.dump(json_list, json_file, indent=4, ignore_nan=True)