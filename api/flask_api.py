"""
Brevets RESTful API
"""
import os
from flask import Flask
from flask_restful import Api
from mongoengine import connect
# You need to implement two resources: Brevet and Brevets.
# Uncomment when done:
# from resources.brevet import Brevet
# from resources.brevets import Brevets

# Connect MongoEngine to mongodb
connect(host=f"mongodb://{os.environ['MONGODB_HOSTNAME']}:27017/brevetsdb")

# Start Flask app and Api here:
app = flask.Flask(__name__)
# api = 

# Bind resources to paths here:
# api.add_resource(...)


app.debug = os.environ['DEBUG']
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    port = os.environ['PORT']
    print("Opening for global access on port {}".format(port))
    app.run(port=port, host="0.0.0.0")
