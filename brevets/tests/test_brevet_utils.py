"""
Nose tests for mongo_utils.py
"""

#imports for what we need to test
import brevet_utils

#import stuff needed for unit testing database stuff
import os

#named this way so it's clear it doesn't count towards the number of unit tests for actual database stuff
def test_0_brevet_equal_not_equal():
    brevet1 = brevet_utils.Brevet(300, "2025-12-12T09:00")
    brevet2 = brevet_utils.Brevet(300, "2025-12-12T09:00")
    
    brevet3 = brevet_utils.Brevet(300, "2025-12-12T09:00")

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

def test_1_blank_brevet_to_dict():
    brevet = brevet_utils.Brevet(200, "2056-5-5T01:02")

    assert brevet.toDict() == {"length": 200, "start_time": "2056-5-5T01:02", "checkpoints": []}

def test_2_basic_checkpoint_to_dict():
    brevet = brevet_utils.Brevet(200, "2056-5-5T01:02")

    brevet.addCheckpoint(0, "2056-5-5T01:02", "2056-5-5T02:02")

    assert brevet.toDict() == {"length": 200, "start_time": "2056-5-5T01:02", "checkpoints": [
        {"distance": 0, "open_time": "2056-5-5T01:02", "close_time": "2056-5-5T02:02"}
        ]}


def test_3_checkpoint_location_to_dict():
    brevet = brevet_utils.Brevet(200, "2056-5-5T01:02")

    brevet.addCheckpoint(0, "2056-5-5T01:02", "2056-5-5T02:02", "paris")

    assert brevet.toDict() == {"length": 200, "start_time": "2056-5-5T01:02", "checkpoints": [
        {"distance": 0, "open_time": "2056-5-5T01:02", "close_time": "2056-5-5T02:02", "location": "paris"}
        ]}
    
def test_4_from_dict_equals():
    brevet = brevet_utils.Brevet(200, "2056-5-5T01:02")

    brevet.addCheckpoint(0, "2056-5-5T01:02", "2056-5-5T02:02", "paris")

    assert brevet_utils.Brevet(sourceDict = brevet.toDict()) == brevet


