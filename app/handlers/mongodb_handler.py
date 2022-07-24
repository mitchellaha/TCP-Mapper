# ALSO SEE /utils/tcr_utils.py
# ALSO SEE /utils/mongo_utils.py

import datetime as dt
import json
import os
from pprint import pprint as pp

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


MONGO_CLIENT = MongoClient(os.getenv("MONGO_SRV_URL"))

class TCR_Mongo:
    def __init__(self, Collection: str):
        """
        Initializes the MongoDB handler.
        
        params
        ------
        Collection: str
            Name of the collection to use in the database. eg. tickets or customers."""
        if Collection == "customers":
            self.MONGO_COLLECTION = MONGO_CLIENT.tcr.customers
            self.ID_KEY = "CustomerID"
        elif Collection == "tickets":
            self.MONGO_COLLECTION = MONGO_CLIENT.tcr.tickets
            self.ID_KEY = "TicketID"

    def check_if_exists(self, DictionaryToCheck: dict, UID: int = None):
        """
        Checks if a dictionary already exists in the MongoDB database.

        params
        ------
        DictionaryToCheck: dict
            Dictionary to check for existence in the database. Must contain the CustomerID/TicketID key.
        ID: int
            ID of the dictionary to check for existence in the database. eg. CustomerID/TicketID
        """
        if UID is None:
            UID = DictionaryToCheck[self.ID_KEY]
        if self.MONGO_COLLECTION.find_one({self.ID_KEY: UID}) is not None:
            return True
        else:
            return False

    def find_one(self, UID: int):
        """
        Gets a ticket from the MongoDB database with the given UID (TicketID/CustomerID).

        params
        ------
        UID: int
            TicketID/CustomerID to get from the database.
        """
        return self.MONGO_COLLECTION.find_one({self.ID_KEY: UID})

    def update_one(self, DictionaryToUpdate: dict):
        """
        Updates a single dictionary in the MongoDB database. The dictionary must contain the TicketID/CustomerID key.
        """
        self.MONGO_COLLECTION.update_one({self.ID_KEY: DictionaryToUpdate[self.ID_KEY]}, {"$set": DictionaryToUpdate})

    def insert_one(self, DictionaryToInsert: dict):
        """
        Inserts a single dictionary into the MongoDB database.
        """
        self.MONGO_COLLECTION.insert_one(DictionaryToInsert)

    def insert_many(self, DictionaryList: list, SplitBy: int = 1000):
        """
        Inserts a list of dictionaries into the MongoDB database in batches of SplitBy.
        """
        totalCount = len(DictionaryList)
        for i in range(0, totalCount, SplitBy):
            self.MONGO_COLLECTION.insert_many(DictionaryList[i:i + SplitBy])


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

    def check_if_exists(self, Path: str):
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

    def find_one(self, DictionaryToFind: dict, Path: str = None):
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





# ! Split Class Functionality Graveyard Below
# class PDF_Mongo:
#     MONGO_PDF_COLLECTION = MONGO_CLIENT.pdf.files

#     def __init__(self):
#         pass

#     def check_if_exists(self, Path: str):
#         """
#         Checks if a path already exists in the MongoDB database.

#         params
#         ------
#         Path: str
#             Path to check in the MongoDB database.
#         """
#         if self.MONGO_PDF_COLLECTION.find_one({"Path": Path}) is not None:
#             return True
#         else:
#             return False

#     def find_one(self, DictionaryToFind: dict, Path: str = None):
#         """
#         Finds a single dictionary in the MongoDB database.

#         params
#         ------
#         DictionaryToFind: dict
#             Dictionary to find in the MongoDB database.
#         Path: str (optional)
#             Path to find in the MongoDB database.
#         """
#         if Path is None:
#             Path = DictionaryToFind["Path"]
#         return self.MONGO_PDF_COLLECTION.find_one({"Path": Path})

#     def update_one(self, DictionaryToUpdate: dict):
#         """
#         Updates a single dictionary in the MongoDB database.

#         params
#         ------
#         DictionaryToUpdate: dict
#             Dictionary to update in the MongoDB database.
#         """
#         self.MONGO_PDF_COLLECTION.update_one({"Path": DictionaryToUpdate["Path"]}, {"$set": DictionaryToUpdate})

#     def insert_one(self, DictionaryToInsert: dict):
#         """
#         Inserts a single dictionary into the MongoDB database.

#         params
#         ------
#         DictionaryToInsert: dict
#             Dictionary to insert into the MongoDB database.
#         """
#         self.MONGO_PDF_COLLECTION.insert_one(DictionaryToInsert)

#     def insert_many(self, DictionaryList: list, SplitBy: int = None):
#         """
#         Inserts a list of dictionaries into the MongoDB database.

#         params
#         ------
#         DictionaryList: list
#             List of dictionaries to insert into the MongoDB database.
#         SplitBy: int (optional)
#             Number of dictionaries to insert into the MongoDB database in each batch.
#             If None, all dictionaries will be inserted into the MongoDB database in one batch.
#         """
#         if SplitBy is None:
#             self.MONGO_PDF_COLLECTION.insert_many(DictionaryList)
#         else:
#             for i in range(0, len(DictionaryList), SplitBy):
#                 self.MONGO_PDF_COLLECTION.insert_many(DictionaryList[i:i + SplitBy])


# class TCP_Mongo:
#     MONGO_TCP_COLLECTION = MONGO_CLIENT.tcp.files

#     def __init__(self):
#         pass

#     def check_if_exists(self, Path: str):
#         """
#         Checks if a path already exists in the MongoDB database.

#         params
#         ------
#         Path: str
#             Path to check in the MongoDB database.
#         """
#         if self.MONGO_TCP_COLLECTION.find_one({"Path": Path}) is not None:
#             return True
#         else:
#             return False

#     def find_one(self, DictionaryToFind: dict, Path: str = None):
#         """
#         Finds a single dictionary in the MongoDB database.

#         params
#         ------
#         DictionaryToFind: dict
#             Dictionary to find in the MongoDB database.
#         Path: str (optional)
#             Path to find in the MongoDB database.
#         """
#         if Path is None:
#             Path = DictionaryToFind["Path"]
#         return self.MONGO_TCP_COLLECTION.find_one({"Path": Path})

#     def update_one(self, DictionaryToUpdate: dict):
#         """
#         Updates a single dictionary in the MongoDB database.

#         params
#         ------
#         DictionaryToUpdate: dict
#             Dictionary to update in the MongoDB database.
#         """
#         self.MONGO_TCP_COLLECTION.update_one({"Path": DictionaryToUpdate["Path"]}, {"$set": DictionaryToUpdate})

#     def insert_one(self, DictionaryToInsert: dict):
#         """
#         Inserts a single dictionary into the MongoDB database.

#         params
#         ------
#         DictionaryToInsert: dict
#             Dictionary to insert into the MongoDB database.
#         """
#         self.MONGO_TCP_COLLECTION.insert_one(DictionaryToInsert)

#     def insert_many(self, DictionaryList: list, SplitBy: int = None):
#         """
#         Inserts a list of dictionaries into the MongoDB database.

#         params
#         ------
#         DictionaryList: list
#             List of dictionaries to insert into the MongoDB database.
#         SplitBy: int (optional)
#             Number of dictionaries to insert into the MongoDB database in each batch.
#             If None, all dictionaries will be inserted into the MongoDB database in one batch.
#         """
#         if SplitBy is None:
#             self.MONGO_TCP_COLLECTION.insert_many(DictionaryList)
#         else:
#             for i in range(0, len(DictionaryList), SplitBy):
#                 self.MONGO_TCP_COLLECTION.insert_many(DictionaryList[i:i + SplitBy])





# class Ticket_Mongo:
#     MONGO_TICKET_COLLECTION = MONGO_CLIENT.tcr.tickets
#     ID_KEY = "TicketID"

#     def __init__(self):
#         pass

#     def check_if_exists(self, DictionaryToCheck: dict, UID: int = None):
#         """
#         Checks if a dictionary already exists in the MongoDB database.

#         params
#         ------
#         DictionaryToCheck: dict
#             Dictionary to check for existence in the database. Must contain the CustomerID/TicketID key.
#         ID: int
#             ID of the dictionary to check for existence in the database. eg. CustomerID/TicketID
#         """
#         if UID is None:
#             UID = DictionaryToCheck[self.ID_KEY]
#         if self.MONGO_TICKET_COLLECTION.find_one({self.ID_KEY: UID}) is not None:
#             return True
#         else:
#             return False

#     def find_one(self, UID: int):
#         """
#         Gets a ticket from the MongoDB database with the given UID (TicketID/CustomerID).

#         params
#         ------
#         UID: int
#             TicketID/CustomerID to get from the database.
#         """
#         return self.MONGO_TICKET_COLLECTION.find_one({self.ID_KEY: UID})

#     def update_one(self, DictionaryToUpdate: dict):
#         """
#         Updates a single dictionary in the MongoDB database. The dictionary must contain the TicketID/CustomerID key.
#         """
#         self.MONGO_TICKET_COLLECTION.update_one({self.ID_KEY: DictionaryToUpdate[self.ID_KEY]}, {"$set": DictionaryToUpdate})

#     def insert_one(self, DictionaryToInsert: dict):
#         """
#         Inserts a single dictionary into the MongoDB database.
#         """
#         self.MONGO_TICKET_COLLECTION.insert_one(DictionaryToInsert)

#     def insert_many(self, DictionaryList: list, SplitBy: int = 1000):
#         """
#         Inserts a list of dictionaries into the MongoDB database in batches of SplitBy.
#         """
#         totalCount = len(DictionaryList)
#         for i in range(0, totalCount, SplitBy):
#             self.MONGO_TICKET_COLLECTION.insert_many(DictionaryList[i:i + SplitBy])

# class Customer_Mongo:
#     MONGO_CUSTOMER_COLLECTION = MONGO_CLIENT.tcr.customers
#     ID_KEY = "CustomerID"

#     def __init__(self):
#         pass

#     def check_if_exists(self, DictionaryToCheck: dict, UID: int = None):
#         """
#         Checks if a dictionary already exists in the MongoDB database.

#         params
#         ------
#         DictionaryToCheck: dict
#             Dictionary to check for existence in the database. Must contain the CustomerID/TicketID key.
#         UID: int
#             UID of the dictionary to check for existence in the database. eg. CustomerID/TicketID
#         """
#         if UID is None:
#             UID = DictionaryToCheck[self.ID_KEY]
#         if self.MONGO_CUSTOMER_COLLECTION.find_one({self.ID_KEY: UID}) is not None:
#             return True
#         else:
#             return False

#     def find_one(self, CustomerID: int):
#         """
#         Gets a customer from the MongoDB database with the given CustomerID.
#         """
#         return self.MONGO_CUSTOMER_COLLECTION.find_one({self.ID_KEY: CustomerID})

#     def update_one(self, DictionaryToUpdate: dict):
#         """
#         Updates a single dictionary in the MongoDB database.
#         """
#         self.MONGO_CUSTOMER_COLLECTION.update_one({self.ID_KEY: DictionaryToUpdate[self.ID_KEY]}, {"$set": DictionaryToUpdate})

#     def insert_one(self, DictionaryToInsert: dict):
#         """
#         Inserts a single dictionary into the MongoDB database.
#         """
#         self.MONGO_CUSTOMER_COLLECTION.insert_one(DictionaryToInsert)

#     def insert_many(self, DictionaryList: list, SplitBy: int = 1000):
#         """
#         Inserts a list of dictionaries into the MongoDB database in batches of SplitBy.
#         """
#         totalCount = len(DictionaryList)
#         for i in range(0, totalCount, SplitBy):
#             self.MONGO_CUSTOMER_COLLECTION.insert_many(DictionaryList[i:i + SplitBy])
