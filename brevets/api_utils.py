import os
import arrow

import brevet_utils
from brevet_utils import Brevet

import requests


class ApiDatabase:
    """Can save and load a single brevet."""
    def __init__(self, api_address, api_port, logger=None):
        self.api_path = f"http://{api_address}:{api_port}/api/"
        self.logs = []
        self.logger = None

    def DumpLogs(self, debug = False):
        rslt = "\n Api Database:"
        #basic info
        if(debug):
            rslt += "api_path={}".format(self.api_path)
        rslt += "\n Logs:\n"
        for log in self.logs:
            rslt += log + "\n"
        return rslt

    def __log(self, info):
        if(self.logger != None):
            self.logger.info(info)
        else:
            self.logs += [str(info)]

    def StoreBrevet(self, brevet):
        """Stores the brevet as a new item in the database. Returns the id if successful, or None if not"""
        #turn brevet to dict with times convertible to dateTime.
        _id = requests.post("{}/brevets".format(self.api_path), json=brevet.toDict("dateTime")).json()

        return _id

    def GetLatestBrevet(self):
        """Get the stored brevet.

        Returns None if there is no brevet stored.
        Throws an error if something else goes wrong."""
        try:
            items = requests.get("{}/brevets".format(self.api_path)).json()

            self.__log(items)

            # lists should be a list of dictionaries.
            # we just need the last one:
            brevetDict = items[-1]

            #brevet utils can convert the time automatically
            brevet = Brevet(sourceDict = brevetDict)

            return brevet

        except IndexError as e:
            self.__log("Failed to get latest: no items")
            return None
        except Exception as e:
            self.__log("Failed to get latest: ")
            self.__log(e)
            raise
        

    def GetBrevets(self):    
        try:
            items = requests.get("{}/todolists".format(self.api_path)).json()

            brevets = [Brevet(sourceDict = item) for item in items]

            return brevets

        except Exception as e:
            self.__log("Failed to get brevets: ")
            self.__log(e)
            raise

    def GetBrevet(self, brevetId):
        """Returns the specified brevet, or None if not found"""
        self.__logDebug("Failed to get brevet from id: API isn't ready yet")
        return None

    def DeleteBrevet(self, brevetId):
        """Deletes the stored brevet."""
        raise NotImplementedError("API isn't ready yet")
        db.get_collection(self.collectionName).find_one_and_delete({})
