from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()


MONGO_CLIENT = MongoClient(os.getenv("MONGO_SRV_URL"))

def insert_list_mongoDB(FileList: list, Database: str, SplitBy: int = 100):
    """
    Inserts a list of files into the database
    """
    db = MONGO_CLIENT[Database]
    listLength = len(FileList)
    # Split the list into chunks of 500
    for fileGroup in range(0, listLength, SplitBy):
        db.files.insert_many(FileList[fileGroup:fileGroup+SplitBy])
        print("Inserted: " + str(fileGroup) + " to " + str(fileGroup+SplitBy) + " of " + str(listLength))

    # # Insert the fileList into the database
    # db.files.insert_many(FileList)

def insert_one_mongoDB(FileDict, Database):
    """
    Checks for Duplicates and adds to MongoDB if not found
    """
    db = MONGO_CLIENT[Database]

    # Insert the file into the database
    db.files.insert_one(FileDict)

def update_one_mongoDB(FileDict, Database):
    """
    Updates a file in the database
    """
    db = MONGO_CLIENT[Database]
    db.files.update_one({"Path": FileDict["Path"]}, {"$set": FileDict})

def does_file_exist_mongoDB(FilePath, Database):  # TODO: Add a Check For File Size Maybe? To See if its been overwritten/edited
    """
    Checks if the FilePath exists in the database.
    
    params
    ------
    FilePath: string
        Path to the file
    Database: string
        Name of the database

    returns
    -------
    exists: boolean
        True if the file exists in the database, False otherwise
    """
    db = MONGO_CLIENT[Database]
    if db.files.find_one({"Path": FilePath}):
        return True
    else:
        return False

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
