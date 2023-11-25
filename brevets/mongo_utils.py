import os
import arrow
from pymongo import MongoClient

import brevet_utils

#client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
#db = client.mydb


class SingleBrevetDatabase:
    """Can save and load a single brevet."""
    def __init__(self, collectionName):
        self.collectionName = collectionName

    def StoreBrevet(self, brevet):
        """Stores the brevet in the database, replacing any already there."""
        raise NotImplementedError("Database not supported, use API container instead")
    
        #db.get_collection(self.collectionName).replace_one({}, brevet.toDict(), True)
        

    def GetBrevet(self):
        """Get the stored brevet.

        Returns None if there is no brevet stored.
        Throws an error if something else goes wrong."""
        raise NotImplementedError("Database not supported, use API container instead")
        try:
            documents = db.get_collection(self.collectionName).find()

            document = documents.next()

            brevet = Brevet(sourceDict = document)

            brevet.setImmutable()

            return brevet

        except StopIteration:
            return None
    

    def DeleteBrevet(self):
        """Deletes the stored brevet."""
        raise NotImplementedError("Database not supported, use API container instead")
        db.get_collection(self.collectionName).find_one_and_delete({})
