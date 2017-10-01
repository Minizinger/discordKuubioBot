import json
import os
from pymongo import MongoClient

with MongoClient(os.environ.get('MONGO_ADDRESS')) as client:
    with open('reactions.json') as reactions:
        reactions = json.load(reactions)
        client['kb_dynamic']['reactions'] = reactions

    with open('responses.json') as responses:
        responses = json.load(responses)
        client['kb_dynamic']['responses'] = responses
