import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


MONGO_CLIENT = MongoClient(os.getenv("MONGO_SRV_URL"))


class FILE_Mongo:
    def __init__(self, Collection: str):
        """
        Initializes the MongoDB handler.
        
        params
        ------
        Collection: str
            Name of the collection to use in the database. eg. pdf or tcp.
        """
        if Collection == "pdf":
            self.MONGO_COLLECTION = MONGO_CLIENT.pdf.files
        if Collection == "tcp":
            self.MONGO_COLLECTION = MONGO_CLIENT.tcp.files

    def check_if_exists(self, Path: str) -> bool:
        """
        Checks if a path already exists in the MongoDB database.

        params
        ------
        Path: str
            Path to check in the MongoDB database.
        """
        if self.MONGO_COLLECTION.find_one({"Path": Path}) is not None:
            return True
        else:
            return False

    def find_one(self, DictionaryToFind: dict, Path: str = None) -> dict:
        """
        Finds a single dictionary in the MongoDB database.

        params
        ------
        DictionaryToFind: dict
            Dictionary to find in the MongoDB database. Must contain the Path key.
        Path: str (optional)
            Path to find in the MongoDB database.
        """
        if Path is None:
            Path = DictionaryToFind["Path"]
        return self.MONGO_COLLECTION.find_one({"Path": Path})

    def update_one(self, DictionaryToUpdate: dict):
        """
        Updates a single dictionary in the MongoDB database.

        params
        ------
        DictionaryToUpdate: dict
            Dictionary to update in the MongoDB database. Must contain the Path key.
        """
        self.MONGO_COLLECTION.update_one({"Path": DictionaryToUpdate["Path"]}, {"$set": DictionaryToUpdate})

    def insert_one(self, DictionaryToInsert: dict):
        """
        Inserts a single dictionary into the MongoDB database.

        params
        ------
        DictionaryToInsert: dict
            Dictionary to insert into the MongoDB database.
        """
        self.MONGO_COLLECTION.insert_one(DictionaryToInsert)

    def insert_many(self, DictionaryList: list, SplitBy: int = None):
        """
        Inserts a list of dictionaries into the MongoDB database.

        params
        ------
        DictionaryList: list
            List of dictionaries to insert into the MongoDB database.
        SplitBy: int (optional)
            Number of dictionaries to insert into the MongoDB database in each batch.
            If None, all dictionaries will be inserted into the MongoDB database in one batch.
        """
        if SplitBy is None:
            self.MONGO_COLLECTION.insert_many(DictionaryList)
        else:
            for i in range(0, len(DictionaryList), SplitBy):
                self.MONGO_COLLECTION.insert_many(DictionaryList[i:i + SplitBy])

    def delete_one(self, DictionaryToDelete: dict, Path: str = None):
        """
        Deletes a single dictionary from the MongoDB database.

        params
        ------
        DictionaryToDelete: dict
            Dictionary to delete from the MongoDB database. Must contain the Path key.
        """
        if Path is None:
            Path = DictionaryToDelete["Path"]
        self.MONGO_COLLECTION.delete_one({"Path": Path})


    def get_everyone_owner(self):
        """
        Lists all the files in monogoDB where the owner is "everyone".

        All File Paths Returned need to be re-run once network drive is connected fully.

        params
        ------
        Database: string
            Name of the database

        returns
        -------
        files: list
            List of file paths where the MongoDB owner is "everyone"
        """
        return [file["Path"] for file in self.MONGO_COLLECTION.find({"Owner": "Everyone"}, {"_id": 0, "Path": 1})]
