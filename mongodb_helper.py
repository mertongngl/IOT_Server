from pymongo import MongoClient


class MongodbHelper:

    def __init__(self, collection_name: str, db_dsn: str, db_name: str):
        self.collection_name = collection_name
        self.db_name = db_name
        self.db_dsn=db_dsn
        self.client = MongoClient(self.db_dsn)
        self.db = self.client[self.db_name]

    def __get_collection(self):
        return self.db[self.collection_name]

    def list(self, predicate):
        result = self.__get_collection().find(predicate)
        return result

    def add(self, data):
        result = self.__get_collection().insert_one(data)
        return result.inserted_id

    def edit(self, predicate, data):
        result = self.__get_collection().update_one(predicate, {"$set": data})
        return result.modified_count

    def remove(self, predicate):
        result = self.__get_collection().delete_one(predicate)
        return result.deleted_count

    def remove_all(self):
        result = self.__get_collection().delete_many({})
        return result.deleted_count