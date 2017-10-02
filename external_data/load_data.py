import json
import os
from pymongo import MongoClient

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

with MongoClient(os.environ.get('MONGO_ADDRESS')) as client:
    with open(os.path.join(__location__, 'reactions.json')) as reactions:
        reactions = json.load(reactions)
        client['kb_dynamic']['reactions'].update_one({"name": "reactions"}, {"$set": reactions}, True)

    with open(os.path.join(__location__, 'responses.json')) as responses:
        responses = json.load(responses)
        client['kb_dynamic']['responses'].update_one({"name": "responses"}, {"$set": responses}, True)
