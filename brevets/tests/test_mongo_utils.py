"""
Nose tests for mongo_utils.py
"""

#imports for what we need to test
import mongo_utils

#import stuff needed for unit testing database stuff
#doesn't work
from pymongo import MongoClient
import os

#named this way so it's clear it doesn't count towards the number of unit tests for actual database stuff
def test_neg_1_brevet_equal_not_equal():
    brevet1 = mongo_utils.Brevet(300, "2025-12-12T09:00")
    brevet2 = mongo_utils.Brevet(300, "2025-12-12T09:00")
    
    brevet3 = mongo_utils.Brevet(300, "2025-12-12T09:00")

    brevet1.addCheckpoint(0, "2025-12-12T09:00", "2025-12-12T10:00")
    brevet2.addCheckpoint(100, "2025-12-12T11:56", "2025-12-12T15:40")
    
    assert brevet1 != brevet2
    assert brevet1 != brevet3
    assert brevet2 != brevet3

    brevet3.addCheckpoint(0, "2025-12-12T09:00", "2025-12-12T10:00")

    assert brevet1 != brevet2
    assert brevet1 == brevet3
    assert brevet2 != brevet3
    
    brevet3.addCheckpoint(100, "2025-12-12T11:56", "2025-12-12T15:40")
    brevet2.addCheckpoint(0, "2025-12-12T09:00", "2025-12-12T10:00")

    assert brevet1 != brevet2
    assert brevet1 != brevet3
    assert brevet2 == brevet3

    brevet1.addCheckpoint(100, "2025-12-12T11:56", "2025-12-12T15:40")

    assert brevet1 == brevet2
    assert brevet1 == brevet3
    assert brevet2 == brevet3

#a store and retrieve test
#this is a black box test case
def test_0_basic_brevet():
    brevet = mongo_utils.Brevet(300, "2025-12-12T09:00")

    checkpoints = [
        (0, "2025-12-12T09:00", "2025-12-12T10:00"),
        (100, "2025-12-12T11:56", "2025-12-12T15:40"),
        (150, "2025-12-12T13:25", "2025-12-12T19:00"),
        (225, "2025-12-12T15:40", "2025-12-13T00:00"),
        (280, "2025-12-12T17:23", "2025-12-13T03:40"),
        (330, "2025-12-12T18:00", "2025-12-13T05:00"),
        ]

    for c in checkpoints:
        brevet.addCheckpoint(c[0],c[1],c[2])
        
    
    db = mongo_utils.SingleBrevetDatabase("unit_test_0")

    db.StoreBrevet(brevet)

    loadedBrevet = db.GetBrevet()

    assert brevet == loadedBrevet

#edge case test: empty database
#this is a black box test case
def test_1_empty_and_delete():
    db = mongo_utils.SingleBrevetDatabase("unit_test_1_empty")

    db.DeleteBrevet()

    assert db.GetBrevet() is None

    brevet = mongo_utils.Brevet(300, "2025-12-12T09:00")

    db.StoreBrevet(brevet)

    assert db.GetBrevet() is not None

    db.DeleteBrevet()

    assert db.GetBrevet() is None

#the insert test case
#this is a white box test case
def test_2_insert():
    
    brevet = mongo_utils.Brevet(200, "2025-12-12T09:00")

    
    brevet.addCheckpoint(0, "2025-12-12T09:00", "2025-12-12T10:00")
        
    db = mongo_utils.SingleBrevetDatabase("unit_test_2_insert")

    db.StoreBrevet(brevet)

    client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)

    loadedDict = client.mydb.unit_test_2_insert.find({}).next()

    savedDict = brevet.toDict()
    

    assert savedDict["dist"] == loadedDict["dist"] and savedDict["startTime"] == loadedDict["startTime"] and savedDict["checkpoints"] == loadedDict["checkpoints"]

#the retrieve test case
#this is a white box test case
def test_3_retrieve():

    savedDict = {"dist":200, "startTime":"2025-12-12T09:00", "checkpoints":[
                                                  {"dist":0, "openTime":"2025-12-12T09:00", "closeTime":"2025-12-12T10:00"}
                                                           ]}

    client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)

    
    client.mydb.unit_test_3_retrieve.insert_one(savedDict)
    db = mongo_utils.SingleBrevetDatabase("unit_test_3_retrieve")
    
    loadedDict = db.GetBrevet().toDict()

    assert savedDict["dist"] == loadedDict["dist"] and savedDict["startTime"] == loadedDict["startTime"] and savedDict["checkpoints"] == loadedDict["checkpoints"]


    




    
