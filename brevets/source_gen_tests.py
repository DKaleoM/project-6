import flask

def gen_tests(raw_tests):
    #items 0 and 1 are metadata
    runningOffset = 0
    for tests_def in raw_tests:
        #dist is item 0
        brevet_dist = tests_def[0][0]
        start_time = tests_def[0][1]
        
        set_name = tests_def[1][0]
        set_desc_base = tests_def[1][1]
        #item desc is item 2

        final_desc = [set_desc_base, "Bevet dist: {}, Start Time: {}".format(brevet_dist,start_time)]

        tests = gen_tests_set(tests_def, runningOffset)

        yield test_set(set_name, final_desc, tests)

        #items 0 and 1 are metadata
        #sets are opening and closing pairs
        runningOffset += 2*(len(tests_def) - 2);

def gen_tests_set(tests_def, idOffset):
    brevet_dist = tests_def[0][0]
    start_time = tests_def[0][1]

    #items 0 and 1 are metadata
    for i in range(2,len(tests_def)):
        test = tests_def[i]

        #each i is two items
        #and i starts at value 2
        pairStartId = idOffset + (2*(i-2))

        yield from gen_test_pair(start_time, brevet_dist, test, pairStartId)

def gen_test_pair(startTime, brevDist, checkpoint, idOffset):
    dist = checkpoint[0]
    openTime = checkpoint[1]
    closeTime = checkpoint[2]

    
    if len(checkpoint)==3:
        description = "test {{}} time of checkpoint {dist}km (brevet dist: {brev_dist}km)".format(dist= dist, brev_dist= brevDist)
    else:
        description = checkpoint[3]

    yield test_entry(startTime, brevDist, dist, "open", openTime, description.format("open"), idOffset)
    yield test_entry(startTime, brevDist, dist, "close", closeTime, description.format("close"), idOffset + 1)

class test_entry:
    def __init__(self, startTime, brevDist, checkDist, timeType, correctTime, comment, idNum):
        self.start_date = startTime
        self.brev_dist = brevDist
        self.check_dist = checkDist
        self.timeType = timeType
        self.time = correctTime
        self.comment = comment
        self.id_num = idNum

    def __str__(self):
        return "dist: "+str(self.check_dist)+", type: "+self.timeType

class test_set:
    def __init__(self, name, desc, tests):
        self.name = name
        self.desc = desc
        self.tests = tests

def create_tests_py():
    raw_tests = [
        #format: each test set is a list
        #first item is a tuple of dist and start time, since that's const in a brevet
        #second item is a tuple of the name and description strings of the test set
        #items after that are tuples of dist, open time, close time of a checkpoint
        #the intention is, one test set represents one brevet
        #todo: better format for this?
        #todo: why not just use json?
        [
            ("Test Set 1: Basic 300km brevet", "Single brevet with times generated using the online calculator"),
            (300, "2025-12-12T09:00"),
            (0, "2025-12-12T09:00", "2025-12-12T10:00"),
            (100, "2025-12-12T11:56", "2025-12-12T15:40"),
            (150, "2025-12-12T13:25", "2025-12-12T19:00"),
            (225, "2025-12-12T15:40", "2025-12-13T00:00"),
            (280, "2025-12-12T17:23", "2025-12-13T03:40"),
            (330, "2025-12-12T18:00", "2025-12-13T05:00"),
        ],
        [
            
            ("Test Set 2: Basic 1000km brevet", "Single brevet with times generated using the online calculator"),
            (1000, "2035-05-06T15:00"),
            (0, "2035-05-06T15:00", "2035-05-06T16:00"),
            (300, "2035-05-07T00:00", "2035-05-07T11:00"),
            (600, "2035-05-07T09:48", "2035-05-08T07:00"),
            (900, "2035-05-07T20:31", "2035-05-09T09:15"),
            (1100, "2035-05-08T00:05", "2035-05-09T18:00"),
        ],
        [
            ("Test Set 3: short times", "Generated using the online calculator, to test the edge cases under 60km."),
            (200, "2035-07-06T12:00"),
            (0, "2035-07-06T12:00", "2035-07-06T13:00"),
            (20, "2035-07-06T12:35", "2035-07-06T14:00"),
            (40, "2035-07-06T13:11", "2035-07-06T15:00"),
            (50, "2035-07-06T13:28", "2035-07-06T15:30"),
            (60, "2035-07-06T13:46", "2035-07-06T16:00"),
            (70, "2035-07-06T14:04", "2035-07-06T16:40"),
        ],
        [
            ("Test Set 4: times over brevet dist", "Tests to make sure times for distances over the brevet dist are same as at the brevet dist."),
            (200, "2035-07-06T12:00"),
            (200, "2035-07-06T17:53", "2035-07-07T01:30"),
            (205, "2035-07-06T17:53", "2035-07-07T01:30"),
            (212, "2035-07-06T17:53", "2035-07-07T01:30"),
            (222, "2035-07-06T17:53", "2035-07-07T01:30"),
        ],
        [
            ("Test Set 5: decimal distances", "Tests to make sure distances are rounded the same as the online calculator https://rusa.org/octime_acp.html"),
            (200, "2050-01-01T00:00"),
            (99, "2050-01-01T02:55", "2050-01-01T06:36"),
            (99.4, "2050-01-01T02:55", "2050-01-01T06:36"),
            (99.6, "2050-01-01T02:56", "2050-01-01T06:40"),
            (100, "2050-01-01T02:56", "2050-01-01T06:40"),
        ]
        #todo: a way to do misc ones would be nice
        ]

    disclaimer_text ='''This code was partially generated using the JINJA templating engine.
    All the other work is still my own, including how I decide the template parameters
    Source gen code can be found (possibly commented out) in flask_brevets.py
    So look there for a better breakdown of the test cases
    '''

    return flask.render_template("tests.py", test_sets=gen_tests(raw_tests))
