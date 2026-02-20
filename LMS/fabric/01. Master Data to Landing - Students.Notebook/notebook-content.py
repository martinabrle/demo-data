# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# MARKDOWN ********************

# **Import libraries**

# CELL ********************

from pyspark.sql import SparkSession
import requests
import base64
import os

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Initialize parameters**

# CELL ********************


spark = SparkSession.builder.appName("GitHubRepoDownload").getOrCreate()

GITHUB_TREE_URL = (
    "https://api.github.com/repos/martinabrle/demo-data/git/trees/main?recursive=1"
)
OUTPUT_DIR = "./downloaded_repo_spark"
TARGET_PREFIX = "LMS/core_data/students/"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Fetch the list of student files**

# CELL ********************


# Fetch tree JSON (driver)
tree_json = requests.get(GITHUB_TREE_URL).json()
# Convert tree to DataFrame
files_df = spark.createDataFrame(tree_json["tree"]).filter("type = 'blob'").filter(f"path LIKE '{TARGET_PREFIX}%'")
display(files_df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# **Download file and save it into ADLS gen2**

# MARKDOWN ********************

