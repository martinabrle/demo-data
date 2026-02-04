import pandas as pd
import simplejson as json

# Read CSV files
product_categories_df = pd.read_csv('../ProductCategories.csv', names=['productCategoryId', 'createdBy', 'createdDateTime'], dtype={'createdBy': 'str', 'modifiedBy': 'str', 'createdDateTime': 'str'}, skiprows=1)
product_categories_df.insert(1,'entityType', 'ProductCategory')
product_category_texts_df = pd.read_csv('../ProductCategoryTexts.csv', names=['productCategoryId', 'languageId', 'shortDescription', 'mediumDescription', 'longDescription'], skiprows=1)
product_category_texts_df.insert(0,'entityType', 'ProductCategoryTexts')

# Convert product texts to dictionary grouped by productCategoryId
product_category_texts_grouped = product_category_texts_df.groupby('productCategoryId').apply(lambda x: x.to_dict(orient='records')).to_dict()

# Merge product texts into products
product_categories_df['texts'] = product_categories_df['productCategoryId'].map(product_category_texts_grouped)

# Convert to list of dictionaries
json_list = product_categories_df.to_dict(orient='records')

# Write to JSON file
with open('productCategories.json', 'w') as json_file:
    json.dump(json_list, json_file, indent=4, ignore_nan=True)