import os
import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB running on the host machine
client = MongoClient("mongodb://192.168.1.8:27017/")
db = client['hvac']

# Directory containing the CSV files
csv_directory = '/home/satya/hvac_mobile/.github/data'

# Iterate over all CSV files in the directory
for filename in os.listdir(csv_directory):
    if filename.endswith(".csv"):
        # Create collection name from the filename (remove .csv extension)
        collection_name = os.path.splitext(filename)[0]
        
        # Read CSV file into DataFrame
        csv_path = os.path.join(csv_directory, filename)
        df = pd.read_csv(csv_path)
        
        # Convert DataFrame to dictionary
        data = df.to_dict(orient='records')
        
        # Insert data into MongoDB collection
        collection = db[collection_name]
        collection.insert_many(data)

print("All CSV files have been imported into MongoDB collections.")
