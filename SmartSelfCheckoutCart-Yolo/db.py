from pymongo import MongoClient

# Local MongoDB connection
client = MongoClient("mongodb://localhost:27017/")

# Database name
db = client["smart_self_checkout"]

# Collections
orders_col = db["orders"]
users_col = db["users"]
products_col = db["products"]


print("✅ Connected to Local MongoDB")
