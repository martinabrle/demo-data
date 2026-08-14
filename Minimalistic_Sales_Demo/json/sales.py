import pandas as pd
import simplejson as json

# Read CSV files
sales_df = pd.read_csv('../sales.csv', names=['Transaction_ID','Customer_ID','Product_ID','Quantity_Sold','Unit_Price','Total_Price','Timestamp'], dtype={'Transaction_ID': 'str', 'Customer_ID': 'str', 'Product_ID': 'str', 'Quantity_Sold': 'str', 'Unit_Price': 'str', 'Total_Price': 'str', 'Timestamp': 'str'}, skiprows=1)
sales_df.insert(1,'entityType', 'Sales')

sales_dict = sales_df.set_index('Transaction_ID').to_dict(orient='records')

# Write to JSON file
with open('sales.json', 'w') as json_file:
    json.dump(sales_dict, json_file, indent=4, ignore_nan=True)