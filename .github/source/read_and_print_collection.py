from pymongo import MongoClient

# Connect to MongoDB running on the host machine
client = MongoClient("mongodb://host.docker.internal:27017/")
db = client['hvac']

# Get list of collections in the hvac database
collection_names = db.list_collection_names()

# Iterate over each collection
for collection_name in collection_names:
    print(f"Collection: {collection_name}")
    
    # Get the collection
    collection = db[collection_name]
    
    # Retrieve and print each record in the collection
    for record in collection.find():
        print(record)
    print("\n")

print("All records have been printed.")
