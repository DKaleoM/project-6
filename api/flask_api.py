"""
Brevets RESTful API
"""
import os
from flask import Flask
from flask_restful import Api
from mongoengine import connect
#Two resources: Brevet and Brevets.
# Uncomment when done:
from resources.brevet import BrevetResource
from resources.brevets import BrevetsResource

import logging

# Connect MongoEngine to mongodb
connect(host=f"mongodb://{os.environ['MONGODB_HOSTNAME']}:27017/brevetsdb")

# Start Flask app and Api here:
app = Flask(__name__)
api = Api(app)

# Bind resources to paths here:
api.add_resource(BrevetsResource, "/api/brevets")
api.add_resource(BrevetResource, "/api/brevet/<id>")


app.debug = os.environ['DEBUG']
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    port = os.environ['PORT']
    print("Opening for global access on port {}".format(port))
    app.run(port=port, host="0.0.0.0")
