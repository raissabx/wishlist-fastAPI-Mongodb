from pymongo import MongoClient

client = MongoClient("mongodb+srv://raissabxdev:201295@cluster0.xcetukc.mongodb.net/?retryWrites=true&w=majority")

db = client['API Wishlist']

collection_client = db['client_collection']
collection_product = db['product_collection']

