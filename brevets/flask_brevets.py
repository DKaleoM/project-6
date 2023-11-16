"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import source_gen_tests  #testing code source generation
from source_gen_tests import create_tests_py

import mongo_utils #for saving and loading brevets

import json #to parse requests sent to us

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

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
    brevet = mongo_utils.Brevet(brevet_dist, time_str)
    
    for i in range(len(km_vals)):
        brevet.addCheckpoint(km_vals[i],open_vals[i],close_vals[i])
        
    #add brevet as only item in collection "brevet"
    db = mongo_utils.SingleBrevetDatabase("brevet")
    
    db.StoreBrevet(brevet)

    #return success
    return flask.jsonify(succeeded = True)

@app.route("/_times", methods=['GET'])
def _get_times():
    #fetch brevet
    db = mongo_utils.SingleBrevetDatabase("brevet")
    brevet = db.GetBrevet()

    if brevet is None:
        #special case with no brevet
        return flask.jsonify(succeeded = False, msg="No brevet saved yet!")

    #return brevet
    return flask.jsonify(succeeded = True, result=brevet.toDict())


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
