import os
import arrow
from pymongo import MongoClient

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.mydb


class SingleBrevetDatabase:
    """Can save and load a single brevet."""
    def __init__(self, collectionName):
        self.collectionName = collectionName

    def StoreBrevet(self, brevet):
        """Stores the brevet in the database, replacing any already there."""
        
        db.get_collection(self.collectionName).replace_one({}, brevet.toDict(), True)
        

    def GetBrevet(self):
        """Get the stored brevet.

        Returns None if there is no brevet stored.
        Throws an error if something else goes wrong."""
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
        db.get_collection(self.collectionName).find_one_and_delete({})



#todo: move Brevet to a BrevetUtils file

#these classes just store the data basically
#so there's a bit more structure
#I... look forward to project 6
    
class Brevet:
    """Stores the data related to an already calculated brevet"""
    def __init__(self, dist=None, startTime=None, sourceDict = None):
        """Takes brevet dist and start time parameters, add checkpoints with addCheckpoint(data).

        Alternatively, provide a source dict to load it as a brevet."""
        #todo: documentation for shorthand
        self.__immutable = False;

        if sourceDict is not None:
            dist = sourceDict["dist"]
            startTime = sourceDict["startTime"]
            self.checkpoints = sourceDict["checkpoints"]
        else:
            self.checkpoints = []

        assert dist is not None, "missing dist parameter"
        assert startTime is not None, "missing startTime parameter"
        
        assert dist in [200,300,400,600,1000], "invalid brevet dist"
        if isinstance(startTime, arrow.arrow.Arrow):
            startTime = startTime.format('YYYY-MM-DDTHH:mm')

        self.dist = dist
        self.startTime = startTime
        

    def isImmutable(self):
        """Returns True if the Brevet is immutable, and False otherwise"""
        return self.__immutable;

    def setImmutable(self):
        """Flags the Brevet as immutable, which will prevent checkpoints from being added."""
        self.__immutable = True;

    def addCheckpoint(self,dist,openTime,closeTime):
        """Adds an already calculated checkpoint to the brevet. Throws AttributeError if the brevet is immutable."""
        if self.__immutable:
            raise AttributeError("Tried to modify immutable Brevet")
        
        self.checkpoints += [{"dist":dist,"openTime":openTime,"closeTime":closeTime}]

    def getCheckpoints(self):
        """Returns the checkpoints as a list of dictionaries"""
        return self.checkpoints

    def toDict(self):
        """Returns a dictionary representation of the brevet"""
        data = {"dist":self.dist, "startTime":self.startTime}

        checkpoints = []

        for checkpoint in self.checkpoints:
            checkpoints += [checkpoint]

        data["checkpoints"] = checkpoints

        return data

    def __eq__(self, other):
        #I'm too tired to even think about if this is even slightly acceptable
        #but my guess would be no
        list1 = [tuple([(k, v) for k, v in dictionary.items()]) for dictionary in self.checkpoints]
        list2 = [tuple([(k, v) for k, v in dictionary.items()]) for dictionary in other.checkpoints]
        return self.dist == other.dist and self.startTime == other.startTime and set(list1) == set(list2)

    def __ne__(self,other):
        return not self.__eq__(other)

    def __str__(self):
        text = "Brevet{dist="+str(self.dist)+", startTime:"+self.startTime+", checkpoins:[";
        for checkpoint in self.checkpoints:
            text+=str(checkpoint)+", "
        text += "]}"
        return text

    """
    def __setattr__(self, name, value):
        if __immutable:
            raise AttributeError("Tried to modify immutable Brevet")
        else:
            super().__setattr__(name, value)
    """
