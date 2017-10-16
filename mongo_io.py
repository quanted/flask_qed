import sys
from pymongo import MongoClient
from flask_restful import Resource

class MongoIO(Resource):
    def __init__(self):
        self.result = None


    def insert_into_db(self, dct_inputs_outputs):
        try:
            client = MongoClient("mongodb://127.0.0.1:27017")
            db = client.primer
            self.result = db.models.insert_one(dct_inputs_outputs)
        except:
            print("Unexpected error:", sys.exc_info()[0])



