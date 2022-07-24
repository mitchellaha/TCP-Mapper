from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()


MONGO_CLIENT = MongoClient(os.getenv("MONGO_SRV_URL"))

def list_everyone_owner_mongoDB(Database):
    """
    Lists all the files in monogoDB where the owner is "everyone".

    params
    ------
    Database: string
        Name of the database

    returns
    -------
    files: list
        List of file paths where the MongoDB owner is "everyone"
    """
    db = MONGO_CLIENT[Database]
    return [file["Path"] for file in db.files.find({"Owner": "Everyone"}, {"_id": 0, "Path": 1})]
