# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "6f4189fd-1e9b-4b03-b188-66b54ecf0c9b",
# META       "default_lakehouse_name": "LH_Bikes",
# META       "default_lakehouse_workspace_id": "1a7264cf-5a08-47ab-aa00-41a6f005f2d3",
# META       "known_lakehouses": [
# META         {
# META           "id": "6f4189fd-1e9b-4b03-b188-66b54ecf0c9b"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# ### Import libraries

# CELL ********************

from pyspark.sql.functions import lit, to_date, col
from pyspark import SparkFiles
from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType, DateType, DecimalType
from pyspark.sql.functions import first
from notebookutils import mssparkutils
import requests
import base64
import os

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Initialize parameters

# CELL ********************

GITHUB_PATH = (
    "https://martinabrle.github.io/martinabrle/Sample_Bike_Sales_Demo/"
)
KEYVAULT_NAME="https://martinabrlefabricdemo.vault.azure.net/"
WORKSPACE_NAME = "demo-bike-sales"
LANGUAGES = ["EN","FR","DE","ES"]
LANGUAGE_NAMES = {
    "EN": "English",
    "FR": "French",
    "DE": "German",
    "ES": "Spanish"
}

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

AZURE_TENANT_ID = mssparkutils.credentials.getSecret(KEYVAULT_NAME, "azure-tenant-id")
AZURE_CLIENT_ID = mssparkutils.credentials.getSecret(KEYVAULT_NAME, "azure-client-id")
AZURE_CLIENT_SECRET = mssparkutils.credentials.getSecret(KEYVAULT_NAME, "azure-client-secret")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Load Addresses

# CELL ********************

file_name="Addresses.csv"

schema = StructType([
    StructField("address_id", IntegerType(), False, metadata={"description": "Unique identifier for the address", "comment": "Address identifier", "display_name": "Address ID", "primary_key": True}),
    StructField("city", StringType(), True, metadata={"description": "City of the address", "comment": "City name", "display_name": "City"}),
    StructField("postal_code", StringType(), True, metadata={"description": "Postal code of the address", "comment": "Postal code", "display_name": "Postal Code"}),
    StructField("street", StringType(), True, metadata={"description": "Street name of the address", "comment": "Street name", "display_name": "Street"}),
    StructField("building", StringType(), True, metadata={"description": "Building number of the address", "comment": "Building number", "display_name": "Building"}),
    StructField("country", StringType(), True, metadata={"description": "Country of the address", "comment": "Country code", "display_name": "Country"}),
    StructField("region", StringType(), True, metadata={"description": "Administrative region, state, or province", "comment": "Region code", "display_name": "Region"}),
    StructField("address_type", StringType(), True, metadata={"description": "Classification of the address such as billing, shipping, or home", "comment": "Address type", "display_name": "Address Type"}),
    StructField("validity_start_date", StringType(), True, metadata={"description": "Date from which the address is considered valid", "comment": "VValidity start date", "display_name": "Valid From"}),
    StructField("validity_end_date", StringType(), True, metadata={"description": "Date until which the address is considered valid", "comment": "Validity end date", "display_name": "Valid To"}),
    StructField("latitude", DoubleType(), True, metadata={"description": "Geographical latitude coordinate of the address", "comment": "Latitude", "display_name": "Latitude"}),
    StructField("longitude", DoubleType(), True, metadata={"description": "Geographical longitude coordinate of the address", "comment": "Longitude", "display_name": "Longitude"})
])

gh_full_file_name = f"{GITHUB_PATH}/{file_name}"
display(f"Downloading {gh_full_file_name}")

sc.addFile(gh_full_file_name)
gh_file_name  = 'file://' +SparkFiles.get(file_name)

addresses_df = spark.read.csv(path=gh_file_name,header=True,schema=schema)
print(f"Downloaded data {gh_file_name} - {addresses_df.count()} rows")

addresses_df = addresses_df.withColumn("validity_start_date", to_date(col("validity_start_date"), "yyyyMMdd"))
addresses_df = addresses_df.withColumn("validity_end_date", to_date(col("validity_end_date"), "yyyyMMdd"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Load Employees and Employee Addresses

# CELL ********************

file_name="Employees.csv"

schema = StructType([
    StructField("employee_id", IntegerType(), False, metadata={"description": "Unique identifier of the employee", "comment": "Employee identifier", "display_name": "Employee ID", "primary_key": True}),
    StructField("first_name", StringType(), True, metadata={"description": "Employee's first name", "comment": "First name", "display_name": "First Name"}),
    StructField("middle_name", StringType(), True, metadata={"description": "Employee's middle name", "comment": "Middle name", "display_name": "Middle Name"}),
    StructField("last_name", StringType(), True, metadata={"description": "Employee's last name", "comment": "Last name", "display_name": "Last Name"}),
    StructField("initials", StringType(), True, metadata={"description": "Employee initials", "comment": "Initials", "display_name": "Initials"}),
    StructField("country", StringType(), True, metadata={"description": "Country associated with the employee", "comment": "Country", "display_name": "Country"}),
    StructField("gender", StringType(), True, metadata={"description": "Gender of the employee", "comment": "Gender", "display_name": "Gender"}),
    StructField("language", StringType(), True, metadata={"description": "Preferred language of the employee", "comment": "Language", "display_name": "Language"}),
    StructField("phone_no", StringType(), True, metadata={"description": "Employee phone number", "comment": "Phone number", "display_name": "Phone Number"}),
    StructField("email", StringType(), True, metadata={"description": "Employee email address", "comment": "Email address", "display_name": "Email"}),
    StructField("login_name", StringType(), True, metadata={"description": "Login name used by the employee", "comment": "Login name", "display_name": "Login Name"}),
    StructField("address_id", IntegerType(), True, metadata={"description": "Identifier of the employee's address", "comment": "Address identifier", "display_name": "Address ID"}),
    StructField("validity_start_date", StringType(), True, metadata={"description": "Date from which the employee record is valid", "comment": "Validity start date", "display_name": "Valid From"}),
    StructField("validity_end_date", StringType(), True, metadata={"description": "Date until which the employee record is valid", "comment": "Validity end date", "display_name": "Valid To"})
])

gh_full_file_name = f"{GITHUB_PATH}/{file_name}"
display(f"Downloading {gh_full_file_name}")

sc.addFile(gh_full_file_name)
gh_file_name  = 'file://' +SparkFiles.get(file_name)

employees_df = spark.read.csv(path=gh_file_name,header=True,schema=schema)
print(f"Downloaded data {gh_file_name} - {employees_df.count()} rows")

employees_df = employees_df.withColumn("validity_start_date", to_date(col("validity_start_date"), "yyyyMMdd"))
employees_df = employees_df.withColumn("validity_end_date", to_date(col("validity_end_date"), "yyyyMMdd"))

employees_df \
    .write \
    .option("description","Employee records") \
    .option("display_name","Employees") \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("employees")

df_employee_addresses = addresses_df.join(
    employees_df,
    on="address_id",
    how="left_semi"
)

df_employee_addresses \
    .write \
    .format("delta") \
    .option("description","Work addresses of employees") \
    .option("display_name","Employee Addresses") \
    .mode("overwrite") \
    .saveAsTable("employee_addresses")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Load Customers and Customer Addresses

# CELL ********************

file_name="Customers.csv"

schema = StructType([
    StructField("customer_id", IntegerType(), False, metadata={"description": "Unique identifier of the customer", "comment": "Customer identifier", "display_name": "Customer ID", "primary_key": True}),
    StructField("email", StringType(), True, metadata={"description": "Customer email address", "comment": "Email address", "display_name": "Email"}),
    StructField("phone_no", StringType(), True, metadata={"description": "Customer phone number", "comment": "Phone number", "display_name": "Phone Number"}),
    StructField("fax_no", StringType(), True, metadata={"description": "Customer fax number", "comment": "Fax number", "display_name": "Fax Number"}),
    StructField("url", StringType(), True, metadata={"description": "Customer website or URL", "comment": "Website URL", "display_name": "Website"}),
    StructField("address_id", IntegerType(), True, metadata={"description": "Identifier of the customer's address", "comment": "Address identifier", "display_name": "Address ID"}),
    StructField("company_name", StringType(), True, metadata={"description": "Legal or registered name of the company", "comment": "Company name", "display_name": "Customer"}),
    StructField("legal_form", StringType(), True, metadata={"description": "Legal form of the company, such as Ltd or Inc", "comment": "Legal form", "display_name": "Legal Form"}),
    StructField("created_by", IntegerType(), True, metadata={"description": "Identifier of the user who created the customer record", "comment": "Created by", "display_name": "Created By"}),
    StructField("created_date", StringType(), True, metadata={"description": "Date when the customer record was created", "comment": "Created date", "display_name": "Created Date"}),
    StructField("modified_by", IntegerType(), True, metadata={"description": "Identifier of the user who last modified the customer record", "comment": "Modified by", "display_name": "Modified By"}),
    StructField("modified_date", StringType(), True, metadata={"description": "Date when the customer record was last modified", "comment": "Modified date", "display_name": "Modified Date"}),
    StructField("currency", StringType(), True, metadata={"description": "Default currency associated with the customer", "comment": "Currency", "display_name": "Currency" })
])

gh_full_file_name = f"{GITHUB_PATH}/{file_name}"
display(f"Downloading {gh_full_file_name}")

sc.addFile(gh_full_file_name)
gh_file_name  = 'file://' +SparkFiles.get(file_name)

customers_df = spark.read.csv(path=gh_file_name,header=True,schema=schema)
print(f"Downloaded data {gh_file_name} - {customers_df.count()} rows")

customers_df = customers_df.withColumn("created_date", to_date(col("created_date"), "yyyyMMdd"))
customers_df = customers_df.withColumn("modified_date", to_date(col("modified_date"), "yyyyMMdd"))

customers_df \
    .write \
    .option("description","Customer records") \
    .option("display_name","Customers") \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("customers")

df_customer_addresses = addresses_df.join(
    customers_df,
    on="address_id",
    how="left_semi"
)

df_customer_addresses \
    .write \
    .option("description","Addresses of customers") \
    .option("display_name","Customer Addresses") \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("customer_addresses")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Load Vendors and Vendor Addresses

# CELL ********************

file_name="Vendors.csv"

schema = StructType([
    StructField("vendor_id", IntegerType(), False, metadata={"description": "Unique identifier of the vendor", "comment": "Vendor identifier", "display_name": "Vendor ID", "primary_key": True}),
    StructField("email", StringType(), True, metadata={"description": "Vendor email address", "comment": "Email address", "display_name": "Email"}),
    StructField("phone_no", StringType(), True, metadata={"description": "Vendor phone number", "comment": "Phone number", "display_name": "Phone Number"}),
    StructField("fax_no", StringType(), True, metadata={"description": "Vendor fax number", "comment": "Fax number", "display_name": "Fax Number"}),
    StructField("url", StringType(), True, metadata={"description": "Vendor website or URL", "comment": "Website URL", "display_name": "Website"}),
    StructField("address_id", IntegerType(), True, metadata={"description": "Identifier of the vendor address", "comment": "Address identifier", "display_name": "Address ID"}),
    StructField("company_name", StringType(), True, metadata={"description": "Legal or registered name of the vendor company", "comment": "Company name", "display_name": "Vendor"}),
    StructField("legal_form", StringType(), True, metadata={"description": "Legal form of the vendor company, such as Ltd or Inc", "comment": "Legal form", "display_name": "Legal Form"}),
    StructField("created_by", IntegerType(), True, metadata={"description": "Identifier of the user who created the vendor record", "comment": "Created by", "display_name": "Created By"}),
    StructField("created_date", StringType(), True, metadata={"description": "Date when the vendor record was created", "comment": "Created date", "display_name": "Created Date"}),
    StructField("modified_by", IntegerType(), True, metadata={"description": "Identifier of the user who last modified the vendor record", "comment": "Modified by", "display_name": "Modified By"}),
    StructField("modified_date", StringType(), True, metadata={"description": "Date when the vendor record was last modified", "comment": "Modified date", "display_name": "Modified Date"}),
    StructField("currency", StringType(), True, metadata={"description": "Default currency associated with the vendor", "comment": "Currency", "display_name": "Currency"})
])

gh_full_file_name = f"{GITHUB_PATH}/{file_name}"
display(f"Downloading {gh_full_file_name}")

sc.addFile(gh_full_file_name)
gh_file_name  = 'file://' +SparkFiles.get(file_name)

vendors_df = spark.read.csv(path=gh_file_name,header=True,schema=schema)
print(f"Downloaded data {gh_file_name} - {vendors_df.count()} rows")

vendors_df = vendors_df.withColumn("created_date", to_date(col("created_date"), "yyyyMMdd"))
vendors_df = vendors_df.withColumn("modified_date", to_date(col("modified_date"), "yyyyMMdd"))

vendors_df \
    .write \
    .option("description","Vendor records") \
    .option("display_name","Vendors") \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("vendors")

df_vendor_addresses = addresses_df.join(
    vendors_df,
    on="address_id",
    how="left_semi"
)

df_vendor_addresses \
    .write \
    .option("description","Addresses of vendors") \
    .option("display_name","Vendor Addresses") \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("vendor_addresses")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Load Product Categories

# CELL ********************

file_name="ProductCategories.csv"

schema = StructType([
    StructField("product_category_id", StringType(), False, metadata={"description": "Unique identifier of the product category", "comment": "Product category ID", "display_name": "Product Category ID", "primary_key": True}),
    StructField("created_by", IntegerType(), True, metadata={"description": "Identifier of the user who created the product category", "comment": "Created by", "display_name": "Created By"}),
    StructField("created_date", StringType(), True, metadata={"description": "Date when the product category record was created", "comment": "Created date", "display_name": "Created Date"})
])

gh_full_file_name = f"{GITHUB_PATH}/{file_name}"
display(f"Downloading {gh_full_file_name}")

sc.addFile(gh_full_file_name)
gh_file_name  = 'file://' +SparkFiles.get(file_name)

product_categories_df = spark.read.csv(path=gh_file_name,header=True,schema=schema)
print(f"Downloaded data {gh_file_name} - {product_categories_df.count()} rows")

product_categories_df = product_categories_df.withColumn("created_date", to_date(col("created_date"), "yyyyMMdd"))

product_categories_df \
    .write \
    .option("description","Categories of products") \
    .option("display_name","Product Categories") \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("product_categories")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Load Product Category Texts

# CELL ********************

file_name="ProductCategoryTexts.csv"

schema = StructType([
    StructField("product_category_id", StringType(), False, metadata={"description": "Unique identifier of the product category", "comment": "Product category ID", "display_name": "Product Category ID"}),
    StructField("language", StringType(), True, metadata={"description": "Language code for the description", "comment": "Language", "display_name": "Language"}),
    StructField("short_description", StringType(), True, metadata={"description": "Short description of the product category", "comment": "Short description", "display_name": "Short Description"}),
    StructField("medium_description", StringType(), True, metadata={"description": "Medium-length description of the product category", "comment": "Medium description", "display_name": "Medium Description"}),
    StructField("long_description", StringType(), True, metadata={"description": "Long, detailed description of the product category", "comment": "Long description", "display_name": "Long Description"})
])

gh_full_file_name = f"{GITHUB_PATH}/{file_name}"
display(f"Downloading {gh_full_file_name}")

sc.addFile(gh_full_file_name)
gh_file_name  = 'file://' +SparkFiles.get(file_name)

product_category_texts_df = spark.read.csv(path=gh_file_name,header=True,schema=schema)
print(f"Downloaded data {gh_file_name} - {product_category_texts_df.count()} rows")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Transform and write _product_category_names_

# CELL ********************

product_category_names_df = product_category_texts_df.drop('medium_description','long_description')
product_category_names_df = product_category_names_df.withColumn(
    "product_category_name",
    col("short_description").alias(
        "product_category_name",
        metadata={
            "description": "Name of the product category",
            "comment": "Product category name",
            "display_name": "Product Category"})
).drop('short_description')

product_category_names_df = (
    product_category_names_df.groupBy("product_category_id")
      .pivot("language", LANGUAGES)
      .agg(first("product_category_name"))
      .fillna("", subset=LANGUAGES)
)

for lang in LANGUAGES:

    new_column_name=f"product_category_name_{lang.lower()}"
    new_column_description=f"Name of the product category in {LANGUAGE_NAMES[lang]}"
    new_column_comment=f"Product category name in {LANGUAGE_NAMES[lang]}"
    new_column_display_name=f"Product Category ({LANGUAGE_NAMES[lang]})"

    product_category_names_df = product_category_names_df.withColumn(
        new_column_name,
        col(lang).alias(
            new_column_name,
            metadata={
                "description": new_column_description,
                "comment": new_column_comment,
                "display_name": new_column_display_name})
    ).drop(lang)

product_category_names_df \
    .write \
    .option("description","Localized product category names") \
    .option("display_name","Product Category Names") \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("product_category_names")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Transform and write _product_category_descriptions_

# CELL ********************

product_category_medium_desc_df = product_category_texts_df.drop('short_description','long_description')
product_category_long_desc_df = product_category_texts_df.drop('short_description','medium_description')

product_category_medium_desc_df = (
    product_category_medium_desc_df.groupBy("product_category_id")
      .pivot("language", LANGUAGES)
      .agg(first("medium_description"))
      .fillna("", subset=LANGUAGES)
)

product_category_long_desc_df = (
    product_category_long_desc_df.groupBy("product_category_id")
      .pivot("language", LANGUAGES)
      .agg(first("long_description"))
      .fillna("", subset=LANGUAGES)
)

for lang in LANGUAGES:

    new_column_name=f"product_category_medium_description_{lang.lower()}"
    new_column_description=f"Medium description of the product category in {LANGUAGE_NAMES[lang]}"
    new_column_comment=f"Product category medium description in {LANGUAGE_NAMES[lang]}"
    new_column_display_name=f"Product Category Medium Description ({LANGUAGE_NAMES[lang]})"

    product_category_medium_desc_df = product_category_medium_desc_df.withColumn(
        new_column_name,
        col(lang).alias(
            new_column_name,
            metadata={
                "description": new_column_description,
                "comment": new_column_comment,
                "display_name": new_column_display_name})
    ).drop(lang)

for lang in LANGUAGES:

    new_column_name=f"product_category_long_description_{lang.lower()}"
    new_column_description=f"Long description of the product category in {LANGUAGE_NAMES[lang]}"
    new_column_comment=f"Product category long description in {LANGUAGE_NAMES[lang]}"
    new_column_display_name=f"Product Category Long Description ({LANGUAGE_NAMES[lang]})"

    product_category_long_desc_df = product_category_long_desc_df.withColumn(
        new_column_name,
        col(lang).alias(
            new_column_name,
            metadata={
                "description": new_column_description,
                "comment": new_column_comment,
                "display_name": new_column_display_name})
    ).drop(lang)

product_category_descriptions_df = product_category_medium_desc_df.join(
    product_category_long_desc_df,
    on="product_category_id",
    how="inner"
)

product_category_descriptions_df \
    .write \
    .option("description","Localized product category descriptions") \
    .option("display_name","Product Category Descriptions") \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("product_category_descriptions")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Load Products

# CELL ********************

file_name="Products.csv"

schema = StructType([
    StructField("product_id", StringType(), False, metadata={"description": "Unique identifier of the product", "comment": "Product ID", "display_name": "Product ID", "primary_key": True}),
    StructField("type_code", StringType(), True, metadata={"description": "Type code of the product", "comment": "Type code", "display_name": "Type Code"}),
    StructField("product_category_id", StringType(), True, metadata={"description": "Identifier of the product category", "comment": "Product category ID", "display_name": "Product Category ID"}),
    StructField("created_by", IntegerType(), True, metadata={"description": "Identifier of the user who created the product record", "comment": "Created by", "display_name": "Created By"}),
    StructField("created_date", StringType(), True, metadata={"description": "Date when the product record was created", "comment": "Created date", "display_name": "Created Date"}),
    StructField("modified_by", IntegerType(), True, metadata={"description": "Identifier of the user who last modified the product record", "comment": "Modified by", "display_name": "Modified By"}),
    StructField("modified_date", StringType(), True, metadata={"description": "Date when the product record was last modified", "comment": "Modified date", "display_name": "Modified Date"}),
    StructField("vendor_id", IntegerType(), True, metadata={"description": "Identifier of the vendor supplying the product", "comment": "Vendor ID", "display_name": "Vendor ID"}),
    StructField("tax_tariff_code", StringType(), True, metadata={"description": "Tax tariff or classification code for the product", "comment": "Tax tariff code", "display_name": "Tax Tariff Code"}),
    StructField("quantity_unit", StringType(), True, metadata={"description": "Unit of measure for the product quantity", "comment": "Quantity unit", "display_name": "Quantity Unit"}),
    StructField("weight_measure", DoubleType(), True, metadata={"description": "Weight of the product", "comment": "Weight measure", "display_name": "Weight"}),
    StructField("weight_unit", StringType(), True, metadata={"description": "Unit of weight", "comment": "Weight unit", "display_name": "Weight Unit"}),
    StructField("currency", StringType(), True, metadata={"description": "Currency for the product pricing", "comment": "Currency", "display_name": "Currency"}),
    StructField("price", DecimalType(), True, metadata={"description": "Price of the product", "comment": "Price", "display_name": "Price"}),
    StructField("width", DoubleType(), True, metadata={"description": "Width of the product", "comment": "Width", "display_name": "Width"}),
    StructField("depth", DoubleType(), True, metadata={"description": "Depth of the product", "comment": "Depth", "display_name": "Depth"}),
    StructField("height", DoubleType(), True, metadata={"description": "Height of the product", "comment": "Height", "display_name": "Height"}),
    StructField("dimension_unit", StringType(), True, metadata={"description": "Unit for product dimensions", "comment": "Dimension unit", "display_name": "Dimension Unit"}),
    StructField("product_pic_url", StringType(), True, metadata={"description": "URL to the product image", "comment": "Product picture URL", "display_name": "Product Picture URL"})
])

gh_full_file_name = f"{GITHUB_PATH}/{file_name}"
display(f"Downloading {gh_full_file_name}")

sc.addFile(gh_full_file_name)
gh_file_name  = 'file://' +SparkFiles.get(file_name)

products_df = spark.read.csv(path=gh_file_name,header=True,schema=schema)
print(f"Downloaded data {gh_file_name}")

products_df = products_df.withColumn("created_date", to_date(col("created_date"), "yyyyMMdd"))
products_df = products_df.withColumn("modified_date", to_date(col("modified_date"), "yyyyMMdd"))

products_df \
    .write \
    .option("description","Product records") \
    .option("display_name","Products") \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("products")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Load Product Texts

# CELL ********************

file_name="ProductTexts.csv"

schema = StructType([
    StructField("product_id", StringType(), False, metadata={"description": "Unique identifier of the product", "comment": "Product ID", "display_name": "Product ID"}),
    StructField("language", StringType(), False, metadata={"description": "Language code for the product description", "comment": "Language", "display_name": "Language"}),
    StructField("short_description", StringType(), True, metadata={"description": "Short description of the product", "comment": "Short description", "display_name": "Short Description"}),
    StructField("medium_description", StringType(), True, metadata={"description": "Medium-length description of the product", "comment": "Medium description", "display_name": "Medium Description"}),
    StructField("long_description", StringType(), True, metadata={"description": "Long, detailed description of the product", "comment": "Long description", "display_name": "Long Description"})
])

gh_full_file_name = f"{GITHUB_PATH}/{file_name}"
display(f"Downloading {gh_full_file_name}")

sc.addFile(gh_full_file_name)
gh_file_name  = 'file://' +SparkFiles.get(file_name)

product_texts_df = spark.read.csv(path=gh_file_name,header=True,schema=schema)
print(f"Downloaded data {gh_file_name} - {product_texts_df.count()} rows")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Transform and write _product_names_

# CELL ********************

product_names_df = product_texts_df.drop('medium_description','long_description')
product_names_df = product_names_df.withColumn(
    "product_name",
    col("short_description").alias(
        "product_name",
        metadata={
            "description": "Name of the product",
            "comment": "Product name",
            "display_name": "Product"})
).drop('short_description')

product_names_df = (
    product_names_df.groupBy("product_id")
      .pivot("language", LANGUAGES)
      .agg(first("product_name"))
      .fillna("", subset=LANGUAGES)
)

for lang in LANGUAGES:

    new_column_name=f"product_name_{lang.lower()}"
    new_column_description=f"Name of the product in {LANGUAGE_NAMES[lang]}"
    new_column_comment=f"Product name in {LANGUAGE_NAMES[lang]}"
    new_column_display_name=f"Product ({LANGUAGE_NAMES[lang]})"

    product_names_df = product_names_df.withColumn(
        new_column_name,
        col(lang).alias(
            new_column_name,
            metadata={
                "description": new_column_description,
                "comment": new_column_comment,
                "display_name": new_column_display_name})
    ).drop(lang)

product_names_df \
    .write \
    .option("description","Localized product names") \
    .option("display_name","Product Names") \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("product_names")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Transform and write _product_descriptions_

# CELL ********************

product_medium_desc_df = product_texts_df.drop('short_description','long_description')
product_long_desc_df = product_texts_df.drop('short_description','medium_description')

product_medium_desc_df = (
    product_medium_desc_df.groupBy("product_id")
      .pivot("language", LANGUAGES)
      .agg(first("medium_description"))
      .fillna("", subset=LANGUAGES)
)

product_long_desc_df = (
    product_long_desc_df.groupBy("product_id")
      .pivot("language", LANGUAGES)
      .agg(first("long_description"))
      .fillna("", subset=LANGUAGES)
)

for lang in LANGUAGES:

    new_column_name=f"product_medium_description_{lang.lower()}"
    new_column_description=f"Medium description of the product in {LANGUAGE_NAMES[lang]}"
    new_column_comment=f"Product medium description in {LANGUAGE_NAMES[lang]}"
    new_column_display_name=f"Product Medium Description ({LANGUAGE_NAMES[lang]})"

    product_medium_desc_df = product_medium_desc_df.withColumn(
        new_column_name,
        col(lang).alias(
            new_column_name,
            metadata={
                "description": new_column_description,
                "comment": new_column_comment,
                "display_name": new_column_display_name})
    ).drop(lang)

for lang in LANGUAGES:

    new_column_name=f"product_long_description_{lang.lower()}"
    new_column_description=f"Long description of the product in {LANGUAGE_NAMES[lang]}"
    new_column_comment=f"Product long description in {LANGUAGE_NAMES[lang]}"
    new_column_display_name=f"Product Long Description ({LANGUAGE_NAMES[lang]})"

    product_long_desc_df = product_long_desc_df.withColumn(
        new_column_name,
        col(lang).alias(
            new_column_name,
            metadata={
                "description": new_column_description,
                "comment": new_column_comment,
                "display_name": new_column_display_name})
    ).drop(lang)

product_descriptions_df = product_medium_desc_df.join(
    product_long_desc_df,
    on="product_id",
    how="inner"
)

product_descriptions_df \
    .write \
    .option("description","Localized product descriptions") \
    .option("display_name","Product Descriptions") \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("product_descriptions")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Load Sales Orders

# CELL ********************

file_name="SalesOrders.csv"

schema = StructType([
    StructField("sales_order_id", IntegerType(), False, metadata={"description": "Unique identifier of the sales order", "comment": "Sales order ID", "display_name": "Sales Order ID", "primary_key": True}),
    StructField("created_by", IntegerType(), True, metadata={"description": "Identifier of the user who created the sales order", "comment": "Created by", "display_name": "Created By"}),
    StructField("created_date", StringType(), True, metadata={"description": "Date when the sales order was created", "comment": "Created date", "display_name": "Created Date"}),
    StructField("modified_by", IntegerType(), True, metadata={"description": "Identifier of the user who last modified the sales order", "comment": "Modified by", "display_name": "Modified By"}),
    StructField("modified_date", StringType(), True, metadata={"description": "Date when the sales order was last modified", "comment": "Modified date", "display_name": "Modified Date"}),
    StructField("fisc_variant", StringType(), True, metadata={"description": "Fiscal variant associated with the sales order", "comment": "Fiscal variant", "display_name": "Fiscal Variant"}),
    StructField("fiscal_year_period", StringType(), True, metadata={"description": "Fiscal year and period for the sales order", "comment": "Fiscal year period", "display_name": "Fiscal Year/Period"}),
    StructField("note_id", IntegerType(), True, metadata={"description": "Identifier of associated note", "comment": "Note ID", "display_name": "Note ID"}),
    StructField("customer_id", IntegerType(), False, metadata={"description": "Identifier of the customer for this sales order", "comment": "Customer ID", "display_name": "Customer ID"}),
    StructField("sales_org", StringType(), True, metadata={"description": "Sales organization responsible for the order", "comment": "Sales organization", "display_name": "Sales Organization"}),
    StructField("currency", StringType(), True, metadata={"description": "Currency of the sales order amounts", "comment": "Currency", "display_name": "Currency"}),
    StructField("gross_amount", DecimalType(), True, metadata={"description": "Gross amount of the sales order", "comment": "Gross amount", "display_name": "Gross Amount"}),
    StructField("net_amount", DecimalType(), True, metadata={"description": "Net amount of the sales order", "comment": "Net amount", "display_name": "Net Amount"}),
    StructField("tax_amount", DecimalType(), True, metadata={"description": "Tax amount of the sales order", "comment": "Tax amount", "display_name": "Tax Amount"}),
    StructField("lifecycle_status", StringType(), True, metadata={"description": "Lifecycle status of the sales order (In Process, Completed, Cancelled, Unknown)", "comment": "Lifecycle status", "display_name": "Lifecycle Status"}),
    StructField("billing_status", StringType(), True, metadata={"description": "Billing status of the sales order (Not Billed, Partially Billed, Completely Billed, Cancelled, Unknown)", "comment": "Billing status", "display_name": "Billing Status"}),
    StructField("delivery_status", StringType(), True, metadata={"description": "Delivery status of the sales order (Not Delivered, PArtially Delivered, Completely Delivered, Cancelled, Unknown) ", "comment": "Delivery status", "display_name": "Delivery Status"})
])

gh_full_file_name = f"{GITHUB_PATH}/{file_name}"
display(f"Downloading {gh_full_file_name}")

sc.addFile(gh_full_file_name)
gh_file_name  = 'file://' +SparkFiles.get(file_name)

sales_orders_df = spark.read.csv(path=gh_file_name,header=True,schema=schema)
print(f"Downloaded data {gh_file_name}")

sales_orders_df = sales_orders_df.withColumn("created_date", to_date(col("created_date"), "yyyyMMdd"))
sales_orders_df = sales_orders_df.withColumn("modified_date", to_date(col("modified_date"), "yyyyMMdd"))

sales_orders_df = sales_orders_df.withColumn(
    "lifecycle_status",
    F.when(F.col("lifecycle_status") == "I", "In Process")
     .when(F.col("lifecycle_status") == "C", "Completed")
     .when(F.col("lifecycle_status") == "X", "Cancelled")
     .otherwise("Unknown")
)

sales_orders_df = sales_orders_df.withColumn(
    "billing_status",
    F.when(F.col("billing_status") == "N", "Not Billed")
     .when(F.col("billing_status") == "P", "Partially Billed")
     .when(F.col("billing_status") == "C", "Completely Billed")
     .when(F.col("billing_status") == "X", "Cancelled")
     .otherwise("Unknown")
)

sales_orders_df = sales_orders_df.withColumn(
    "delivery_status",
    F.when(F.col("delivery_status") == "N", "Not Delivered")
     .when(F.col("delivery_status") == "P", "Partially Delivered")
     .when(F.col("delivery_status") == "C", "Completely Delivered")
     .when(F.col("delivery_status") == "X", "Cancelled")
     .otherwise("Unknown")
)

sales_orders_df \
    .write \
    .option("description","Sales order records") \
    .option("display_name","Sales Orders") \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("sales_orders")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Load Sales Order Items

# CELL ********************

file_name="SalesOrderItems.csv"

schema = StructType([
    StructField("sales_order_id", IntegerType(), False, metadata={"description": "Identifier of the sales order", "comment": "Sales order ID", "display_name": "Sales Order ID"}),
    StructField("sales_order_item_id", IntegerType(), False, metadata={"description": "Identifier of the sales order item", "comment": "Sales order item ID", "display_name": "Sales Order Item ID"}),
    StructField("product_id", StringType(), False, metadata={"description": "Identifier of the product for this order item", "comment": "Product ID", "display_name": "Product ID"}),
    StructField("note_id", IntegerType(), True, metadata={"description": "Identifier of associated note for this item", "comment": "Note ID", "display_name": "Note ID"}),
    StructField("currency", StringType(), True, metadata={"description": "Currency of the amounts for this order item", "comment": "Currency", "display_name": "Currency"}),
    StructField("gross_amount", DecimalType(), True, metadata={"description": "Gross amount for this order item", "comment": "Gross amount", "display_name": "Gross Amount"}),
    StructField("net_amount", DecimalType(), True, metadata={"description": "Net amount for this order item", "comment": "Net amount", "display_name": "Net Amount"}),
    StructField("tax_amount", DecimalType(), True, metadata={"description": "Tax amount for this order item", "comment": "Tax amount", "display_name": "Tax Amount"}),
    StructField("item_atp_status", StringType(), True, metadata={"description": "Available-to-promise status of the order item (Confirmed, Partially Confirmed, Not Confirmed, Cancelled / Not Relevant, Unknown)", "comment": "Item ATP status", "display_name": "Item ATP Status"}),
    StructField("op_item_pos", StringType(), True, metadata={"description": "Operational item position identifier", "comment": "Operational item position", "display_name": "OP Item Pos"}),
    StructField("quantity", DecimalType(), True, metadata={"description": "Quantity ordered for this item", "comment": "Quantity", "display_name": "Quantity"}),
    StructField("quantity_unit", DecimalType(), True, metadata={"description": "Unit of measure for the ordered quantity", "comment": "Quantity unit", "display_name": "Quantity Unit"}),
    StructField("delivery_date", DateType(), True, metadata={"description": "Planned delivery date for the order item", "comment": "Delivery date", "display_name": "Delivery Date"})
])

gh_full_file_name = f"{GITHUB_PATH}/{file_name}"
display(f"Downloading {gh_full_file_name}")

sc.addFile(gh_full_file_name)
gh_file_name  = 'file://' +SparkFiles.get(file_name)

sales_order_items_df = spark.read.csv(path=gh_file_name,header=True,schema=schema)
print(f"Downloaded data {gh_file_name}")

sales_order_items_df = sales_order_items_df.withColumn("delivery_date", to_date(col("delivery_date"), "yyyyMMdd"))

sales_order_items_df = sales_order_items_df.withColumn(
    "item_atp_status",
    F.when(F.col("item_atp_status") == "C", "Confirmed")
     .when(F.col("item_atp_status") == "P", "Partially Confirmed")
     .when(F.col("item_atp_status") == "N", "Not Confirmed")
     .when(F.col("item_atp_status") == "X", "Cancelled / Not Relevant")
     .otherwise("Unknown")
)
sales_order_items_df \
    .write \
    .option("description","Order items for sales orders") \
    .option("display_name","Sales Order Items") \
    .format("delta") \
    .mode("overwrite") \
    .option("mergeSchema", "true") \
    .saveAsTable("sales_order_items")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Display table info

# CELL ********************

def show_table_metadata(table_name):
    df=spark.table(table_name)
    """
    Prints schema details and metadata for a Spark DataFrame.

    Args:
        df: Spark DataFrame
    """
    print(" ")
    print(" ")
    print(f"Table: {table_name}:")
    for field in df.schema.fields:
        print(f"Column: {field.name}")
        print(f"  Type: {field.dataType}")
        print(f"  Nullable: {field.nullable}")
        # Print metadata nicely if it exists
        if field.metadata:
            for key, value in field.metadata.items():
                print(f"  {key}: {value}")
        else:
            print("  Metadata: None")
        print("-" * 50)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#Check Metadata has been successfully written
show_table_metadata("sales_order_items")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Check data consistency - Vendors

# CELL ********************

vendors_df = spark.table("vendors")
vendor_addresses_df = spark.table("vendor_addresses")

vendors_with_missing_addresses_df = (
    vendors_df
        .join(
            vendor_addresses_df,
            vendors_df.address_id == vendor_addresses_df.address_id,
            how="left_anti"
        )
)

if vendors_with_missing_addresses_df.count() > 0:
    raise Exception("There are vendors with missing addresses")

addresses_with_missing_vendors_df = (
    vendor_addresses_df
        .join(
            vendors_df,
            vendor_addresses_df.address_id == vendors_df.address_id,
            how="left_anti"
        )
)

if addresses_with_missing_vendors_df.count() > 0:
    raise Exception("There are addresses with missing vendors")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Check data consistency - Customers

# CELL ********************

customers_df = spark.table("vendors")
customer_addresses_df = spark.table("vendor_addresses")

customers_with_missing_addresses_df = (
    customers_df
        .join(
            customer_addresses_df,
            customers_df.address_id == customer_addresses_df.address_id,
            how="left_anti"
        )
)

if customers_with_missing_addresses_df.count() > 0:
    raise Exception("There are customers with missing addresses")

addresses_with_missing_customers_df = (
    customer_addresses_df
        .join(
            customers_df,
            customer_addresses_df.address_id == customers_df.address_id,
            how="left_anti"
        )
)

if addresses_with_missing_customers_df.count() > 0:
    raise Exception("There are addresses with missing customers")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Check data consistency - Employees

# CELL ********************

employees_df = spark.table("employees")
employee_addresses_df = spark.table("employee_addresses")

employees_with_missing_addresses_df = (
    employees_df
        .join(
            employee_addresses_df,
            employees_df.address_id == employee_addresses_df.address_id,
            how="left_anti"
        )
)

if employees_with_missing_addresses_df.count() > 0:
    raise Exception("There are employees with missing addresses")

addresses_with_missing_employees_df = (
    employee_addresses_df
        .join(
            employees_df,
            employee_addresses_df.address_id == employees_df.address_id,
            how="left_anti"
        )
)

if addresses_with_missing_employees_df.count() > 0:
    raise Exception("There are addresses with missing employees")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Retrieve access token**

# CELL ********************

import requests

scope = "https://analysis.windows.net/powerbi/api/.default"

url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": scope
}

response = requests.post(url, data=data)
access_token = response.json().get("access_token")
print("Bearer token:", access_token)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import requests

# --- Configuration ---
workspace_name = "demo-bike-sales"
xmla_url = f"https://{workspace_name}.asazure.windows.net/xmla?role=Admin"

# Replace this with a valid bearer token obtained in the notebook

headers = {
    "Content-Type": "text/xml",
    "Authorization": f"Bearer {access_token}"
}

# Minimal XMLA Discover request to list catalogs
xmla_request = """<?xml version="1.0"?>
<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
  <Body>
    <Discover xmlns="urn:schemas-microsoft-com:xml-analysis">
      <RequestType>DBSCHEMA_CATALOGS</RequestType>
      <Restrictions/>
      <Properties/>
    </Discover>
  </Body>
</Envelope>
"""

# Send request
response = requests.post(xmla_url, headers=headers, data=xmla_request)

# Print status and partial content
print("Status Code:", response.status_code)
print("Response (first 500 chars):")
print(response.text[:500])


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from fabric import semantic_model
from sempy.tables import Table

def update_lakehouse_metadata(table_name: str, token: str):
    """
    Connects to a Fabric workspace semantic model, loops over columns
    of the given Lakehouse table, retrieves metadata, and updates 
    description, comment, and display_name.

    Parameters:
        table_name (str): Lakehouse table name (e.g., 'product_texts')
        token (str): Bearer token with XMLA/Admin access
    """
    
    # Load Spark table
    df = spark.table(f"{database_name}.{table_name}")

    # Connect to semantic model
    model = Model(workspace_name=WORKSPACE_NAME,token=token)
    
    # Get the table object
    table = model.get_table(table_name)
    
    print(f"Updating metadata for table: {table_name}")
    
    for field in df.schema.fields:
        col_name = field.name
        col_meta = field.metadata if field.metadata else {}
        
        # Retrieve metadata values
        display_name = col_meta.get("display_name", col_name.replace("_", " ").title())
        description  = col_meta.get("description", "")
        comment      = col_meta.get("comment", "")
        
        # Get the column in the semantic model
        col = table.get_column(col_name)
        
        # Print current and new metadata
        print(f"Column: {col_name}")
        print(f"  Current display_name: {col.display_name}")
        print(f"  Current description: {col.description}")
        print(f"  Current comment: {col.comment}")
        print(f"  New display_name: {display_name}")
        print(f"  New description: {description}")
        print(f"  New comment: {comment}")
        print("-" * 50)
        
        # Update semantic model metadata
        col.display_name = display_name
        col.description = description
        col.comment = comment
        col.save()
    
    update_lakehouse_metadata("products", bearer_token)
    print(f"Metadata update completed for table: {table_name}")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

update_lakehouse_metadata("products", bearer_token, workspace_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Update semantic model's metadata

# CELL ********************

import requests

def update_semantic_model_from_spark(df, xmla_url, bearer_token, database_name, table_name):
    """
    Updates a Fabric / Power BI semantic model table's column properties
    using Spark DataFrame metadata (display_name, description, nullable, comment).
    
    Args:
        df: Spark DataFrame with metadata in schema
        xmla_url: XMLA endpoint URL (Admin role)
        bearer_token: Azure AD access token with workspace permissions
        database_name: Semantic model (dataset) name
        table_name: Table name in the semantic model
    """
    headers = {
        "Content-Type": "text/xml",
        "Authorization": f"Bearer {bearer_token}"
    }

    # Build XMLA payload for multiple columns in one request
    columns_xml = ""
    for field in df.schema.fields:
        column_name = field.name
        display_name = field.metadata.get("display_name", column_name)
        description = field.metadata.get("description", "")
        nullable = str(field.nullable).lower()  # 'true' or 'false'
        comment = field.metadata.get("comment", "")

        # Each column alteration XML
        columns_xml += f"""
        <Column>
            <ColumnID>{column_name}</ColumnID>
            <Name>{display_name}</Name>
            <Description>{description}</Description>
            <IsNullable>{nullable}</IsNullable>
            <Annotations>
                <Annotation>
                    <Name>comment</Name>
                    <Value>{comment}</Value>
                </Annotation>
            </Annotations>
        </Column>
        """

    # Full XMLA request
    xmla_payload = f"""<?xml version="1.0"?>
<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
  <Body>
    <Execute xmlns="urn:schemas-microsoft-com:xml-analysis">
      <Command>
        <Alter xmlns="http://schemas.microsoft.com/analysisservices/2003/engine">
          <Object>
            <DatabaseID>{database_name}</DatabaseID>
            <CubeID>{table_name}</CubeID>
          </Object>
          <AlterCommand>
            <Table>
                {columns_xml}
            </Table>
          </AlterCommand>
        </Alter>
      </Command>
      <Properties>
        <PropertyList>
          <LocaleIdentifier>1033</LocaleIdentifier>
        </PropertyList>
      </Properties>
    </Execute>
  </Body>
</Envelope>
"""

    response = requests.post(xmla_url, headers=headers, data=xmla_payload)
    if response.status_code != 200:
        print(f"Failed to update table {table_name}: {response.text}")
    else:
        print(f"Updated table {table_name} columns successfully!")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import requests

scope = "https://analysis.windows.net/powerbi/api/.default"

url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": scope
}

response = requests.post(url, data=data)
access_token = response.json().get("access_token")
# print("Bearer token:", access_token)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Load Spark DataFrame
df = spark.table("products")

# XMLA endpoint (Admin role)
xmla_url = f"https://{WORKSPACE_NAME}.asazure.windows.net/xmla?role=Admin"
# xmla_url = f"https://asazure.windows.net/xmla?role=Admin&workspaceId=6f4189fd-1e9b-4b03-b188-66b54ecf0c9b"


# Azure AD token
bearer_token = access_token

# Semantic model (dataset) and table
database_name = "test"
table_name = "products"

# Push Spark metadata to semantic model
update_semantic_model_from_spark(df, xmla_url, bearer_token, database_name, table_name)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# spark.sql("TRUNCATE TABLE customer_addresses")
# spark.sql("TRUNCATE TABLE customers")
# spark.sql("TRUNCATE TABLE employee_addresses")
# spark.sql("TRUNCATE TABLE employees")
# spark.sql("TRUNCATE TABLE product_categories")
# spark.sql("TRUNCATE TABLE product_category_texts")
# spark.sql("TRUNCATE TABLE product_texts")
# spark.sql("TRUNCATE TABLE products")
# spark.sql("TRUNCATE TABLE sales_order_items")
# spark.sql("TRUNCATE TABLE sales_orders")
# spark.sql("TRUNCATE TABLE vendor_addresses")
# spark.sql("TRUNCATE TABLE vendors")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
