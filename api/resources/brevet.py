"""
Resource: Brevet
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet

class BrevetResource(Resource):
    #adapted from the example in TodoListRESTful
    def get(self, id):
        brevet = Brevet.objects().get(id=id).to_json()
        return Response(brevet, mimetype="application/json", status=200)
    
    #adapted from the example in TodoListRESTful
    def put(self, id):
        input_json = request.json
        Brevet.objects().get(id=id).update(**input_json)
        return '', 200
    
    #adapted from the example in TodoListRESTful
    def delete(self, id):
        Brevet.objects().get(id=id).delete()
        return '', 200
