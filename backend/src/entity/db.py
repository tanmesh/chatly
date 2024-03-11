from os import environ as env
from pymongo import MongoClient

class DB:
    def __init__(self):
        self.password = env.get("MONGO_PASSWORD")
        self.connection_string = f"mongodb+srv://tanmeshnm:{self.password}@cluster0.6fsxhi2.mongodb.net/"
        self.client = MongoClient(self.connection_string)
        self.db = self.client.chatly
        self.collection = self.db.chatly

    # Create
    def create_document(self, document):
        try:
            result = self.collection.insert_one(document)
        except Exception as e:
            print(e)
        return result.inserted_id

    # Read
    def read_document(self, query):
        document = self.collection.find_one(query)
        return document