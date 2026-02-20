# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# MARKDOWN ********************

# ### 01. Raw to Landing

# PARAMETERS CELL ********************

today_file = 'LMS_09-01-2023.csv'
processed_date = '2024-09-17'

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

account_name = 'martinabrledemodata' # fill in your primary account name
container_name = 'lms-data' # fill in your container name 
relative_path_raw = 'raw' # fill in your relative folder path for RAW folder
relative_path_landing = 'landing' # fill in your relative folder path for RAW folder

adls_path_raw = 'abfss://%s@%s.dfs.core.windows.net/%s' % (container_name, account_name, relative_path_raw) 
adls_path_landing = 'abfss://%s@%s.dfs.core.windows.net/%s' % (container_name, account_name, relative_path_landing) 

adls_full_file_name_raw = f"{adls_path_raw}/{today_file}"

print('Input raw storage path is ', adls_path_raw)
print('Landing storage path is ', adls_path_landing)

print(f"Going to read a file {adls_full_file_name_raw}")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### Reading csv file of Today

# MARKDOWN ********************

# **Set up auth to the ADLS:**

# CELL ********************

# We can use this just as a demo .... or we can just create a shortcut or use the workspace identity or use a copying strategy with mssparkutils.fs.fastcp
KEYVAULT_NAME="https://martinabrlefabricdemo.vault.azure.net/"
AZURE_TENANT_ID = mssparkutils.credentials.getSecret(KEYVAULT_NAME, "lms-azure-tenant-id")
AZURE_CLIENT_ID = mssparkutils.credentials.getSecret(KEYVAULT_NAME, "lms-azure-client-id")
AZURE_CLIENT_SECRET = mssparkutils.credentials.getSecret(KEYVAULT_NAME, "lms-azure-client-secret")

spark.conf.set(f"fs.azure.account.auth.type.{account_name}.dfs.core.windows.net", "OAuth")
spark.conf.set(f"fs.azure.account.oauth.provider.type.{account_name}.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set(f"fs.azure.account.oauth2.client.id.{account_name}.dfs.core.windows.net", AZURE_CLIENT_ID)
spark.conf.set(f"fs.azure.account.oauth2.client.secret.{account_name}.dfs.core.windows.net", AZURE_CLIENT_SECRET)
spark.conf.set(f"fs.azure.account.oauth2.client.endpoint.{account_name}.dfs.core.windows.net", f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/token")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Test we do have access to the landing directory in ADLS container**

# CELL ********************

files = mssparkutils.fs.ls(adls_path_raw)
for file in files:
    print(file.name, file.isDir, file.isFile, file.path, file.size)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import lit
from pyspark import SparkFiles

print(f"Processing file: {adls_full_file_name_raw}")

df = spark.read.csv(path=adls_full_file_name_raw,header=True,inferSchema=True)
print(f"Downloaded data {adls_full_file_name_raw} - {df.count()} rows")

if not df.rdd.isEmpty():
    print(f"The file has data, saving it under {adls_path_landing}")
    df_new = df.withColumn("Processing_Date",lit(processed_date))
    df_new.write.format('csv').option('header','true').partitionBy('Processing_Date').mode('append').save(adls_path_landing)
    print("Data written to landing zone successfully !")
else:
    print('This file contains only header row and no data.')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
