from pymongo import MongoClient

# db_client = MongoClient().local

db_client = MongoClient(
    "mongodb+srv://test:test@cluster0.izci727.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test

# Cliente de nuestra base de datos remota de MongoDB