from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27018")
db = client['API_Wishlist']

collection_customer = db['customer_collection']
collection_product = db['product_collection']

