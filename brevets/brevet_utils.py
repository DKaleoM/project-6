import os
import arrow

#helper function to convert a time to the right format
def formatTimeToStr(time, tFormat):
    """Formats an object representing a time to the string format specified.

    Valid time types: string, arrow, dictionary representing datetime object.
    Valid formats:
    -default: alias for 'YYYY-MM-DDTHH:mm'
    -arrow: alias for 'YYYY-MM-DDTHH:mm'
    -dateTime: alias for 'YYYY-MM-DD HH:mm' """
    if isinstance(time, str):
        time = arrow.get(time, ['YYYY-MM-DDTHH:mm','YYYY-MM-DD HH:mm'])
    elif isinstance(time, arrow.arrow.Arrow):
        time = time#keep as an arrow
    elif isinstance(time, dict):
        time = arrow.get(time["$date"])
    else:
        raise AssertionError("time was invalid type")

    #at this point, time should be an arrow object
    t = tFormat
    if t in ['dateTime', 'python', 'mongo', 'YYYY-MM-DD HH:mm']:
        return time.format('YYYY-MM-DD HH:mm')
    elif t in ['default', 'arrow', 'jquery', 'moment', 'YYYY-MM-DDTHH:mm']:
        return time.format('YYYY-MM-DDTHH:mm')
    else:
        raise AssertionError("tFormat wasn't a supported format")
    
class Brevet:
    """Stores the data related to an already calculated brevet"""
    def __init__(self, dist=None, startTime=None, sourceDict = None):
        """Takes brevet dist and start time parameters, add checkpoints with addCheckpoint(data).

        Alternatively, provide a source dict to load it as a brevet."""
        #todo: documentation for shorthand
        self.__immutable = False;
        
        if sourceDict is not None:
            dist = sourceDict["length"]
            startTime = sourceDict["start_time"]
            self.checkpoints = sourceDict["checkpoints"]
        else:
            self.checkpoints = []

        assert dist is not None, "missing dist parameter"
        assert startTime is not None, "missing startTime parameter"
        
        assert dist in [200,300,400,600,1000], "invalid brevet dist"

        #format the start time to a string
        startTime = formatTimeToStr(startTime, "default")

        self.dist = dist
        self.startTime = startTime

    
    def __processCheckpointDict(self, checkpoint, tFormat = "default"):
        #format open time and close time to strings
        checkpoint["open_time"] = formatTimeToStr(checkpoint["open_time"],tFormat)
        checkpoint["close_time"] = formatTimeToStr(checkpoint["close_time"],tFormat)
        return checkpoint

    def isImmutable(self):
        """Returns True if the Brevet is immutable, and False otherwise"""
        return self.__immutable;

    def setImmutable(self):
        """Flags the Brevet as immutable, which will prevent checkpoints from being added."""
        self.__immutable = True;

    def addCheckpoint(self,dist,openTime,closeTime,location = None):
        """Adds an already calculated checkpoint to the brevet. Throws AttributeError if the brevet is immutable."""
        if self.__immutable:
            raise AttributeError("Tried to modify immutable Brevet")
        
        data = {"distance":dist,"open_time":formatTimeToStr(openTime,"default"),"close_time":formatTimeToStr(closeTime,"default")}

        if location is not None:
            data["location"] = location

        self.checkpoints += [data]

    def getCheckpoints(self):
        """Returns the checkpoints as a list of dictionaries"""
        return self.checkpoints

    def toDict(self, tFormat = "default"):
        """Returns a dictionary representation of the brevet.
        Can optionally have a time format provided."""
        data = {"length":self.dist, "start_time":formatTimeToStr(self.startTime,tFormat)}

        checkpoints = []

        for checkpoint in self.checkpoints:
            checkpoints += [self.__processCheckpointDict(checkpoint,tFormat)]

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
