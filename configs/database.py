import os
from pymongo import MongoClient

from dotenv import load_dotenv

# Load the .env file
load_dotenv();

# ACcess the vaiables
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Make the mongo db connection
client = MongoClient(MONGO_URI);
db = client[DB_NAME]

#Collections
product_collection = db["products"]
order_collection = db['orders']