"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations

import source_gen_tests  #testing code source generation
from source_gen_tests import create_tests_py

import brevet_utils

#import mongo_utils
import api_utils #for saving and loading brevets using the API

import json #to parse requests sent to us
import os #to read environment variables

import logging

###
# Globals
###
app = flask.Flask(__name__)

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
#Source generation using Jinja
#
###############

#disabled for now
#todo: make it export to a connected folder in docker
#instead of as an endpoint on the server
"""


@app.route("/source_gen_tests")
def source_gen_tests():
    with open("generated_tests.py","w") as f:
        contents = create_tests_py()
        f.write(contents)
    
    return flask.send_file("generated_tests.py") 

"""

###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    #read info from the request
    km = request.args.get('km', None, type=float)
    brevet_dist = request.args.get('brevet_dist', None, type=int)
    time_str = request.args.get('start_time',type=str)

    if (km is None):
        return flask.jsonify(succeeded = False, msg = "Error: invalid km value")
    if (brevet_dist is None):
        return flask.jsonify(succeeded = False, msg = "Error: invalid brevet_dist value")
    if (km > brevet_dist * 1.2):
        return flask.jsonify(succeeded = False, msg = "Checkpoint dist more than 20% over brevet dist is invalid")
    

    start_time = arrow.get(time_str,"YYYY-MM-DDTHH:mm")

    #log info for debugging purposes
    app.logger.debug("km={}".format(km))
    app.logger.debug("brevet_dist={}".format(brevet_dist))
    app.logger.debug("time_str={}".format(time_str))
    app.logger.debug("request.args: {}".format(request.args))
    app.logger.debug("start_time={}".format(start_time.format('YYYY-MM-DDTHH:mm')))

    #calculate open and close time
    open_time = acp_times.open_time(km, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')
    
    close_time = acp_times.close_time(km, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')
    
    #return the result
    result = {"open": open_time, "close": close_time}

    app.logger.debug("results={}".format(result))
    
    return flask.jsonify(succeeded = True, result=result)

API_ADDR = os.environ['API_ADDR']
API_PORT = os.environ['API_PORT']
API_DB = api_utils.ApiDatabase(API_ADDR, API_PORT, app.logger)

@app.route("/_times", methods=['POST'])
def _insert_times():
    #we use request.json instead of request.args to get the data
    #because this is a POST request (and it should be json formatted)
    km_vals = request.json['km_vals']
    open_vals = request.json['open_vals']
    close_vals = request.json['close_vals']
    
    brevet_dist = request.json['brevet_dist']
    time_str = request.json['start_time']

    app.logger.debug("request.json: {}".format(request.json))

    #create brevet to store
    brevet = brevet_utils.Brevet(brevet_dist, time_str)
    
    for i in range(len(km_vals)):
        brevet.addCheckpoint(km_vals[i],open_vals[i],close_vals[i])

    app.logger.debug("brevet created")
        
    #add brevet as only item in collection "brevet"
    db = API_DB

    try:
        brevetId = db.StoreBrevet(brevet)
        return flask.jsonify(succeeded = True)
    except Exception as e:
        app.logger.error("db failed to insert brevet!")
        app.logger.error(e)
        app.logger.error(db.DumpLogs(True))
        return flask.jsonify(succeeded = False, msg = str(e))
        
    

@app.route("/_times", methods=['GET'])
def _get_times():
    #fetch brevet
    db = API_DB

    try:
        brevet = db.GetLatestBrevet()

        if brevet is None:
            #special case with no brevet
            return flask.jsonify(succeeded = False, msg="No brevet saved yet!")

        #return brevet
        brevetDict = brevet.toDict()
        app.logger.debug(brevetDict)
        app.logger.debug(arrow.get(brevetDict["start_time"]))
        return flask.jsonify(succeeded = True, result=brevetDict)
    except Exception as e:
        app.logger.error("db failed to insert brevet!")
        app.logger.error(e)
        app.logger.error(db.DumpLogs(True))
        return flask.jsonify(succeeded = False, msg = str(e))


#############

app.debug = os.environ['DEBUG']
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    port = os.environ['PORT']
    print("Opening for global access on port {}".format(port))
    app.run(port=port, host="0.0.0.0")
