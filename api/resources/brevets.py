"""
Resource: Brevets
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet

from flask import current_app

class BrevetsResource(Resource):
    #adapted from the example in TodoListRESTful
    def get(self):
        json_object = Brevet.objects().to_json()
        return Response(json_object, mimetype="application/json", status=200)

    #adapted from the example in TodoListRESTful
    def post(self):
        try:
            # Read the entire request body as a JSON
            # This will fail if the request body is NOT a JSON.
            input_json = request.json

            ## Because input_json is a dictionary, we can do this:
            #title = input_json["title"] # Should be a string
            #items = input_json["items"] # Should be a list of dictionaries
            #result = TodoList(title=title, items=items).save()

            result = Brevet(**input_json).save()
            return {'_id': str(result.id)}, 200
        except Exception as e:
            current_app.logger.error(e)
            raise
