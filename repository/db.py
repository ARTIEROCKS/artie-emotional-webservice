import os
import pymongo


# Function to create and return the mongodb client
def db_client():
    mongo_host = os.environ["APP_MONGO_HOST"]
    mongo_user = os.environ["APP_MONGO_USER"]
    mongo_password = os.environ["APP_MONGO_PASS"]
    mongo_port = os.environ["APP_MONGO_PORT"]
    mongo_db = os.environ["APP_MONGO_DB"]

    return pymongo.MongoClient("mongodb://" + mongo_user + ":" + mongo_password + "@" + mongo_host + ":" + mongo_port + "/" + mongo_db)


class Database:
    def __init__(self, db_collection):
        self.db = "artie"
        self.db_collection = db_collection

    # Function to insert a document into the collection
    def insert(self, data, client=None):

        # If the client has not been received
        if client is None:
            client = db_client()

        collection = client[self.db][self.db_collection]
        document = collection.insert_one(data)
        return document, client

    # Function to search a document from a collection
    def search(self, query, client=None):

        # If the client has not been received
        if client is None:
            client = db_client()

        collection = client[self.db][self.db_collection]
        result = collection.find_one(query)
        return result, client

    # Function to delete a document from a collection
    def delete(self, query, client=None):

        # If the client has not been received
        if client is None:
            client = db_client()

        collection = client[self.db][self.db_collection]
        return collection.delete_many(query), client

    # Function to update a document from a collection
    def update(self, query, new_values, client=None):

        # If the client has not been received
        if client is None:
            client = db_client()

        collection = client[self.db][self.db_collection]
        new_values = {"$set": new_values}
        return collection.update_one(query, new_values), client
