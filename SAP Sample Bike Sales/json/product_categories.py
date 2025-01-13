import pandas as pd
import simplejson as json

# Read CSV files
product_categories_df = pd.read_csv('json/productCategories.csv', dtype={'createdBy': 'str', 'modifiedBy': 'str', 'vendorId': 'str', 'taxTariffCode': 'str', 'width': 'str', 'height': 'str', 'depth': 'str', 'dimensionUnit': 'str', 'productPicUrl': 'str'})
product_category_texts_df = pd.read_csv('json/productCategoryText.csv')

# Convert product texts to dictionary grouped by productCategoryId
product_category_texts_grouped = product_category_texts_df.groupby('productCategoryId').apply(lambda x: x.to_dict(orient='records')).to_dict()

# Merge product texts into products
product_categories_df['texts'] = product_categories_df['productCategoryId'].map(product_category_texts_grouped)

# Convert to list of dictionaries
json_list = product_categories_df.to_dict(orient='records')

# Write to JSON file
with open('json/productCategories.json', 'w') as json_file:
    json.dump(json_list, json_file, indent=4, ignore_nan=True)